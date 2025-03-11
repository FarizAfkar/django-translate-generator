import openpyxl
from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def home(request):
    lang_list=['en', 'id']
    try:
        lang = request.session['lang']
        if lang in lang_list:
            translation.activate(lang)
            request.session['lang'] = lang
        else:
            lang='id'
            translation.activate(lang)
            request.session['lang'] = lang
    finally:
        lang = settings.LANGUAGE_CODE
        if lang in lang_list:
            translation.activate(lang)
            request.session['lang'] = lang
        else:
            lang='id'
            translation.activate(lang)
            request.session['lang'] = lang

    if request.method == 'POST':
        generate = request.POST['generate']
        if generate == 'id':
            gen_col = 1
            filename = 'bilingual_ID.txt'
        else:
            gen_col = 2
            filename = 'bilingual_EN.txt'

        excel_data = list()
        excel_data.append(str(
            'msgid ""\n'
            'msgstr ""\n'
            '"Project-Id-Version: PACKAGE VERSION\\n"\n"'
            'Report-Msgid-Bugs-To: \\n"\n"'
            'POT-Creation-Date: 2022-06-27 11:35+0700\\n"\n"'
            'PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n"'
            'Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n"'
            'Language-Team: LANGUAGE <LL@li.org>\\n"\n"'
            'Language: \\n"\n"'
            'MIME-Version: 1.0\\n"\n"'
            'Content-Type: text/plain; charset=UTF-8\\n"\n"'
            'Content-Transfer-Encoding: 8bit\\n"\n"'
            'Plural-Forms: nplurals=1; plural=0;\\n"\n'))

        file_excel = request.FILES['fileexcel']
        wb = openpyxl.load_workbook(file_excel)
        worksheet = wb['Sheet1']
        for col in worksheet.iter_rows():
            col_data = list()
            for cell in col:
                if(cell.value is None):
                    cell.value=''
                col_data.append(str(cell.value))
            if(col_data[0]!='' and col_data[0]!='msgid' and col_data[gen_col]!=generate):
                excel_data.append(str('msgid "'+col_data[0]+'"'))
                excel_data.append(str('msgstr "'+col_data[gen_col]+'"'+"\n"))

        file_data = "\n".join(excel_data)
        response = HttpResponse(file_data, content_type='application/text charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    context = {
        'title':'Django Translate Generator'
    }

    return render(request, 'tgenerator/home.html', context)

def changelanguage(request, lang):
    translation.activate(lang)
    settings.LANGUAGE_CODE = lang
    settings.LANGUAGE_SESSION_KEY = lang
    request.session['lang'] = lang
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
