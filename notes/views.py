import os
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.http import FileResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note, Report


def notes(request):
    notes = Note.objects.all().order_by("-upload_date")
    return render(request, "notes/notes.html", {"notes": notes})


@login_required
def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    try:
        file_path = note.file.path
    except ValueError:
        raise Http404("File path is invalid.")

    if os.path.exists(file_path):
        note.download_count = note.download_count + 1
        note.save(update_fields=["download_count"])
        return FileResponse(
            open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path)
        )
    else:
        raise Http404("File not found.")


@login_required
def report_note(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(Note, id=note_id)
        reason = request.POST.get("reason", "")
        Report.objects.create(note=note, reported_by=request.user, reason=reason)
        messages.success(request, "Thank you for your report. We will review it shortly.")
        return HttpResponseRedirect(reverse("notes_list"))
    return HttpResponseRedirect(reverse("notes_list"))
