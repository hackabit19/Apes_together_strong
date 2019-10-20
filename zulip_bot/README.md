This is the Zulip Bot on the Zulip Chat organization Apes-together-strong. 
This bot integrates our "ConnectAll" app with the Zulip Chat Platform.

## Instructions on using the Zulip Bot

1. Run backend.
2. Run `python3 play_zulip.py`
3. On the Zulip Chat https://apes-together-strong.zulipchat.com, the user can request the following services : `narrate_book`, `narrate_note`, `create_signs` by pinging the bot with the following commands :
	(i) @ConnectAll narrate_book `<url_of_book_pdf>`
			The bot replies with a link to the audio file of the narration of the book.
	(ii) @ConnectAll narrate_note `<url_of_notes_image>`
			The bot replies with a link to the audio file of the narration of the notes.
			The bot further asks a follow up whether a labelled image of notes with text and bounding boxes is required. 
	(iii) @ConnectAll create_signs `<url_of_audio>`
			The bot replies with a link to the video file of the Sign Language translation of the audio.
