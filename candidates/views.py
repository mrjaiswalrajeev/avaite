from django.db.models import Count, Q, Case, When, IntegerField
from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', '').strip()
        
        if search_query:
            words = [word.strip() for word in search_query.split() if word.strip()]
            if words:
                # Create OR conditions for all words
                or_conditions = Q()
                for word in words:
                    or_conditions |= Q(name__icontains=word)
                
                queryset = queryset.filter(or_conditions)
                
                # Create AND conditions for word count
                and_conditions = Q()
                for word in words:
                    and_conditions &= Q(name__icontains=word)
                
                # Annotate with:
                # 1. exact_match: matches entire query exactly
                # 2. all_words: contains all words (any order)
                # 3. word_count: number of matched words
                queryset = queryset.annotate(
                    exact_match=Case(
                        When(name__iexact=search_query, then=3),
                        default=0,
                        output_field=IntegerField()
                    ),
                    all_words=Case(
                        When(and_conditions, then=2),
                        default=0,
                        output_field=IntegerField()
                    ),
                    word_count=Count(
                        Case(
                            *[When(name__icontains=word, then=1) for word in words],
                            output_field=IntegerField()
                        )
                    )
                ).order_by('-exact_match', '-all_words', '-word_count', 'name')
            else:
                queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('name')
        
        return queryset