from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.db.models import Q


# Create your views here.
from posts.models import Post
from curateGoogleAlerts.models import PrivacyRightsRecord


def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')
            if search_type not in ['google_alerts', 'privacy_rights_record']:
                search_type = 'privacy_rights_record'

        except Exception:
            search_type = 'privacy_rights_record'

        count = {}
        results = {}
        results['google_alerts'] = Post.objects.filter(Q(title__icontains=querystring) | Q(content__icontains=querystring)
            )
        results['privacy_rights_record'] = PrivacyRightsRecord.objects.filter(
            Q(location__icontains=querystring) | Q(
                description__icontains=querystring) | Q(
                    company_name__icontains=querystring) | Q(
                    breach_type__icontains=querystring))
        # results['all'] = results['google_alert_posts'] | results['privacy_rights_record']
        count['google_alerts'] = results['google_alerts'].count()
        count['privacy_rights_record'] = results['privacy_rights_record'].count()
        # count['all'] = results['all'].count()

        paginator = Paginator(results[search_type], 20)
        page = request.GET.get('page')
        try:
            page_results = paginator.page(page)
        except PageNotAnInteger:
            page_results = paginator.page(1)
        except EmptyPage:
            page_results = paginator.page(paginator.num_pages)

        return render(request, 'results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
            'page_results': page_results,
            'page_range': range(20),
        })
    else:
        return render(request, 'search.html', {'hide_search': True})
