from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import generic
from django.db.models import Q

from .models import Sentence, Tag, Review
from .forms import ReviewForm


# Django pagination:
# https://docs.djangoproject.com/en/3.2/topics/pagination/
# https://docs.djangoproject.com/en/3.2/ref/paginator/
# Example:
# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
# Bootstrap3 pagination:
# https://v3.bootcss.com/components/#pagination
class SentenceList(generic.ListView):
    model = Sentence
    template_name = 'words_in_sentences/sentence-list.html'
    context_object_name = 'sentence_list'
    paginate_by = 10
    # queryset = Sentence.objects.all()

    # docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#dynamic-filtering
    def get_queryset(self):
        query = self.request.GET.get('tag')
        if query:
            return Sentence.objects.filter(tags__name=query)
        return Sentence.objects.all()

    # docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tag_list'] = Tag.objects.all().order_by('name')
        return context


def sentence_detail(request, pk, slug=None):
    # sentence = Sentence.objects.get(pk=pk)
    sentence = get_object_or_404(Sentence, pk=pk)
    review_list = Review.objects.filter(sentence__pk=pk)
    # stackoverflow.com/questions/31003934
    if slug != sentence.slug:
        # Either slug is wrong or None
        return redirect(sentence.get_absolute_url())
    if request.method == 'GET':
        return render(request, 'words_in_sentences/sentence-detail.html', {
            'sentence': sentence,
            'review_list': review_list,
            'zip_review_list': zip(range(1, 6), review_list),
        })
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)
        if form.is_valid() and request.user == sentence.author:
            post = form.save(commit=False)
            post.sentence_id = pk
            # post.review_times = len(review_list) + 1
            post.save()
        return redirect(sentence.get_absolute_url())


def search(request):
    # The empty string handles an empty "request"
    query = request.GET.get('q', '')
    if query:
        # https://docs.djangoproject.com/en/3.2/topics/db/queries/
        # Entry.objects.get(headline__icontains='Lennon')
        # SQL equivalent: SELECT ... WHERE headline ILIKE '%Lennon%';
        queryset = (Q(english_sentence__icontains=query))
        results = Sentence.objects.filter(queryset)
    else:
        results = []
    # The context is a dictionary mapping template variable names to Python objects.
    # docs.djangoproject.com/en/3.2/intro/tutorial03//#write-views-that-actually-do-something
    context = {'results': results, 'query': query}
    return render(request, 'words_in_sentences/search.html', context)
