
using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using {/UnrealEngine.com/Temporary/SpatialMath}
using {TextureLibrary}

VideoScreenDevice := class(creative_device):

	var Playing : logic = false
	var CurrentFrame : int = 0

	@editable
	Framerate : int = 10

	@editable
	FrameNamingScheme : string = "cade_"	# what the frame names begin with
	
	@editable
	PlayButton : button_device = button_device{}
	var PlayButtonTransform: transform = transform{}
	var HiddenTransform: transform = transform{}

	ScreenMaterial : Materials.VideoScreenMaterial = Materials.VideoScreenMaterial{}

	@editable
	ScreenObject : creative_prop = creative_prop{}

	@editable
    AudioSpeaker: audio_player_device = audio_player_device{}

	
	SafeSleep(seconds: float)<suspends>:void=
		Start := GetSimulationElapsedTime()
		loop:
			Now := GetSimulationElapsedTime()
			if (Now - Start >= seconds):
				break
			Sleep(0.001)
	
	# play button callback
	Play(Agent: agent):void=
		if(Self.Playing = true):
			set Self.Playing = false
		else:
			set Self.Playing = true
			PlayButton.Disable()
			# if(PlayButton.TeleportTo[Self.HiddenTransform]):
			spawn {Self.PlayVideo()}

	# after finishing the video, return frame and audio to beginning
	ResetVideo():void=
		set Self.CurrentFrame = 0
		# ! No bloody way to reset it to beginning via verse
		# AudioSpeaker

	PlayVideo()<suspends>:void=
		TimeToSleep: float = 1.0 / (Self.Framerate * 1.0)				# this is such a shit language
		var NextTextureName: string = ""
		loop:
			if(Self.Playing = false):									# base case
				break
			
			set Self.CurrentFrame += 1
			set NextTextureName = "{Self.FrameNamingScheme}{Self.CurrentFrame}"
			# Print("{NextTextureName} | FPS: {1.0 / TimeToSleep}")		#! DEBUGGING ONLY
			if (NextTexture := TextureMap[NextTextureName]):
				set ScreenMaterial.VideoTexture = NextTexture
				if(Self.CurrentFrame = 1):
					AudioSpeaker.Play()
			else:
				Self.ResetVideo()										# reset video and audio to beginning
				break													# break if run out of frames

			SafeSleep(TimeToSleep)
		
		AudioSpeaker.Stop()
		set Self.Playing = false
		# if(PlayButton.TeleportTo[Self.PlayButtonTransform]):
			
		PlayButton.Enable()

	OnBegin<override>()<suspends>:void=
		ScreenObject.SetMaterial(ScreenMaterial)
		# Print("Screen Initialized")									#! DEBUGGING ONLY

		set Self.PlayButtonTransform = PlayButton.GetTransform()
		
		var HiddenPos : vector3 = vector3{}
		set HiddenPos.X = 0.0 
		set HiddenPos.Y = 0.0 
		set HiddenPos.Z = 0.0 

		set Self.HiddenTransform.Translation = HiddenPos
		set Self.HiddenTransform.Rotation = Self.PlayButtonTransform.Rotation
		set Self.HiddenTransform.Scale = Self.PlayButtonTransform.Scale

		PlayButton.InteractedWithEvent.Subscribe(Play)