from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import ToDo


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


@login_required
def todo_list(request):
    if request.method == 'POST':
        # 추가 요청 처리
        if 'add_task' in request.POST:  # 추가 버튼 클릭 시
            task_name = request.POST.get('task')
            if task_name:
                ToDo.objects.create(user=request.user, task=task_name)
                print(f"할 일 추가됨: {task_name}")

        # 수정 요청 처리
        if 'edit_task' in request.POST:  # 수정 버튼 클릭 시
            task_id = request.POST.get('task_id')
            updated_task_name = request.POST.get('updated_task')
            if task_id and updated_task_name:
                task = get_object_or_404(ToDo, id=task_id, user=request.user)
                task.task = updated_task_name
                task.save()

        return redirect('todo_list')  # 처리 후 리다이렉트

    incomplete_tasks = ToDo.objects.filter(user=request.user, is_completed=False)
    completed_tasks = ToDo.objects.filter(user=request.user, is_completed=True)

    if not incomplete_tasks.exists() and completed_tasks.exists():
        # 모든 항목 삭제 후 축하 페이지로 이동
        ToDo.objects.filter(user=request.user).delete()
        return redirect('congrats_page')

    return render(request, 'todo/todo_list.html', {
        'tasks': incomplete_tasks,  # 완료되지 않은 할 일
        'completed_tasks': completed_tasks,  # 완료된 할 일
    })

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(ToDo, id=task_id, user=request.user)  # 특정 작업 가져오기
    task.is_completed = not task.is_completed  # 완료 상태 반전
    task.save()  # 변경 사항 저장
    print(f"Task {task.id} status toggled to {task.is_completed}")
    return redirect('todo_list')  # 목록 페이지로 리다이렉트


@login_required
def congrats_page(request):
    has_incomplete_tasks = ToDo.objects.filter(user = request.user, is_completed = False).exists()
    print(f"Incomplete tasks exist: {has_incomplete_tasks}")
    if has_incomplete_tasks:
        return redirect('todo_list')
    return render(request, 'todo/congrats.html', {'message':'You completed all tasks!'})

def signup(request):
    if request.method == 'POST':
        print("POST 요청 받음:", request.POST)
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            print("회원가입 성공")
            return redirect('login')
        else:
            print("폼 유효성 검사 실패:", form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html',{'form':form})

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    
    def get_success_url(self):
        return '/todo'
    
@login_required
def delete_all_tasks(request):
    if request.method == 'POST':
        ToDo.objects.filter(user=request.user).delete()
        return redirect('todo_list')  # 삭제 후 목록으로 리다이렉트
