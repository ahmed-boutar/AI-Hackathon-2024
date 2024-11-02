from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.audio_service import AudioService
from app.core.config import get_settings

router = APIRouter()
audio_service = AudioService()
settings = get_settings()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith('audio/'):
        raise HTTPException(400, "File must be an audio file")
    
    try:
        # Save uploaded file
        temp_file = await audio_service.save_upload_file(file)
        
        # Transcribe to MIDI
        midi_file = audio_service.transcribe_to_midi(temp_file)
        
        # Return MIDI file
        response = FileResponse(
            path=midi_file,
            media_type='audio/midi',
            filename='transcribed.mid'
        )
        
        # Cleanup files after sending response
        response.background = lambda: audio_service.cleanup_files(temp_file, midi_file)
        
        return response
        
    except Exception as e:
        raise HTTPException(500, str(e))