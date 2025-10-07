import React, { useRef, useEffect, useState } from 'react';

const DanceDetector = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const previousFrameRef = useRef(null);
  const audioRef = useRef(null);
  const [isMotionDetected, setIsMotionDetected] = useState(true);
  const [motionLevel, setMotionLevel] = useState(0);
  const [cameraError, setCameraError] = useState(null);
  const [musicStarted, setMusicStarted] = useState(false);
  const motionTimeoutRef = useRef(null);

  useEffect(() => {
    let stream = null;
    let animationId = null;

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480 }
        });
        
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      } catch (error) {
        console.error('Error accessing camera:', error);
        setCameraError('Unable to access camera. Please grant camera permissions.');
      }
    };

    const detectMotion = () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      if (!video || !canvas || video.readyState !== video.HAVE_ENOUGH_DATA) {
        animationId = requestAnimationFrame(detectMotion);
        return;
      }

      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const currentFrame = context.getImageData(0, 0, canvas.width, canvas.height);
      
      if (previousFrameRef.current) {
        const motion = calculateMotion(previousFrameRef.current, currentFrame);
        setMotionLevel(motion);
        
        // Threshold for detecting motion (adjust as needed)
        const MOTION_THRESHOLD = 15;
        
        if (motion > MOTION_THRESHOLD) {
          setIsMotionDetected(true);
          // Restore normal playback speed and pitch
          if (audioRef.current) {
            audioRef.current.playbackRate = 1.0;
          }
          // Clear any existing timeout
          if (motionTimeoutRef.current) {
            clearTimeout(motionTimeoutRef.current);
          }
          // Set new timeout for 1 second of no motion
          motionTimeoutRef.current = setTimeout(() => {
            setIsMotionDetected(false);
            // Dramatically slow down music and lower pitch when not dancing
            if (audioRef.current) {
              audioRef.current.playbackRate = 0.3;
            }
          }, 1000);
        }
      }
      
      previousFrameRef.current = currentFrame;
      animationId = requestAnimationFrame(detectMotion);
    };

    const calculateMotion = (previousFrame, currentFrame) => {
      let motionPixels = 0;
      const threshold = 30; // Pixel difference threshold
      const samplingRate = 10; // Check every 10th pixel for performance
      
      for (let i = 0; i < currentFrame.data.length; i += 4 * samplingRate) {
        const rDiff = Math.abs(currentFrame.data[i] - previousFrame.data[i]);
        const gDiff = Math.abs(currentFrame.data[i + 1] - previousFrame.data[i + 1]);
        const bDiff = Math.abs(currentFrame.data[i + 2] - previousFrame.data[i + 2]);
        
        const avgDiff = (rDiff + gDiff + bDiff) / 3;
        
        if (avgDiff > threshold) {
          motionPixels++;
        }
      }
      
      // Return motion as a percentage
      return (motionPixels / (currentFrame.data.length / (4 * samplingRate))) * 100;
    };

    startCamera();
    
    // Start motion detection after a short delay to allow camera to initialize
    setTimeout(() => {
      detectMotion();
    }, 1000);

    // Cleanup
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
      if (motionTimeoutRef.current) {
        clearTimeout(motionTimeoutRef.current);
      }
    };
  }, []);

  const startMusic = () => {
    if (audioRef.current) {
      console.log('Attempting to play music...');
      audioRef.current.play()
        .then(() => {
          console.log('Music started successfully!');
          setMusicStarted(true);
        })
        .catch(error => {
          console.error('Error playing audio:', error);
          alert('Unable to play music. Error: ' + error.message);
        });
    } else {
      console.error('Audio element not found');
    }
  };

  return (
    <div className="dance-detector">
      <h1>Dance Detector</h1>
      
      {cameraError ? (
        <div className="error">{cameraError}</div>
      ) : (
        <>
          {!musicStarted && (
            <button className="start-button" onClick={startMusic}>
              START MUSIC & DANCE
            </button>
          )}
          
          <div className="video-container">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="video-feed"
            />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            
            {!isMotionDetected && (
              <div className="alert-overlay">
                <div className="alert-message">
                  KEEP DANCING!
                </div>
              </div>
            )}
          </div>
          
          <audio ref={audioRef} loop>
            <source src="/music.mp3" type="audio/mpeg" />
          </audio>
          
          <div className="motion-indicator">
            <div className="motion-bar">
              <div 
                className="motion-fill"
                style={{ 
                  width: `${Math.min(motionLevel * 2, 100)}%`,
                  backgroundColor: isMotionDetected ? '#4ade80' : '#ef4444'
                }}
              />
            </div>
            <div className="status">
              {isMotionDetected ? 'DANCING DETECTED!' : 'NO MOTION DETECTED'}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default DanceDetector;
