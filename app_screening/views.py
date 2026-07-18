from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST

from app_auth.models import Level, Student  

from . models import PlacementQuestion, PlacementResult
from . models import PlacementOption

# ▀▄▀▄ menampilkan daftar question untuk screening awal
def question_list(request):
    user = request.user
   
    placement_questions  = PlacementQuestion.objects.all().order_by('order')
    placement_options   = PlacementOption.objects.all().order_by('order')

    return render(request, 'common/question-list.html', {
        'placement_questions': placement_questions,
        'placement_options' : placement_options,
    }) 

# ▀▄▀▄ json menmpilkan detail melalui modal
def question_detail(request, placement_question_id):

    question = PlacementQuestion.objects.get(pk=placement_question_id)

    return JsonResponse({
        "id": question.id,
        "question": question.question,
        "options": [
            {
                "id": option.id,
                "answer": option.answer,
                "score": option.score
            }
            for option in question.options.all()
        ]
    })

# ▀▄▀▄ json membuat question baru plus option
def question_create(request):
    
    data = json.loads(request.body)

    question = PlacementQuestion.objects.create(
        question=data['question'],
        order=PlacementQuestion.objects.count() + 1
    )

    for index, item in enumerate(data['options'], start=1):

        PlacementOption.objects.create(
            question=question,
            answer=item['answer'],
            score=item['score'],
            order=index
        )

    return JsonResponse({
        'success': True,
        'message': 'Pertanyaan berhasil dibuat'
    })

# ▀▄▀▄ json untuk update question plus option
def question_update(request, question_id):

    if request.method != "POST":
        return JsonResponse({
            "success": False
        })

    data = json.loads(request.body)

    question = PlacementQuestion.objects.get(
        id=question_id
    )

    question.question = data["question"]
    question.save()

    keep_ids = []

    for item in data["options"]:

        option_id = item.get("id")

        if option_id:

            option = PlacementOption.objects.get(
                id=option_id
            )

            option.answer = item["answer"]
            option.score = item["score"]
            option.order = item["order"]
            option.save()

            keep_ids.append(option.id)

        else:

            option = PlacementOption.objects.create(
                question=question,
                answer=item["answer"],
                score=item["score"],
                order=item["order"]
            )

            keep_ids.append(option.id)

    PlacementOption.objects.filter(
        question=question
    ).exclude(
        id__in=keep_ids
    ).delete()

    return JsonResponse({
        "success": True
    })

# ▀▄▀▄ json untuk submit, langsung SAVE level siswa di SESSION
@require_POST
def submit_level_session(request):

    data = json.loads(request.body)
    answers = data.get("answers", {})

    total_score = 0

    for option_id in answers.values():
        try:
            option = PlacementOption.objects.get(id=option_id)
            total_score += option.score
        except PlacementOption.DoesNotExist:
            pass

    levels = list(Level.objects.all())

    if not levels:
        return JsonResponse({"success": False, "message": "No level data"})

    if total_score < 5:
        level = levels[0]
    elif total_score < 10 and len(levels) > 1:
        level = levels[1]
    else:
        level = levels[-1]

    request.session['placement_level_id'] = level.id
    request.session['placement_score'] = total_score

    return JsonResponse({
        "success": True,
        "redirect": "/register/",
        "level": level.name
    })