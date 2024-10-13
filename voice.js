function detectSilence(stream, recognition, onSoundEnd = _=>{}, onSoundStart = _=>{}, silence_delay = 500, min_decibels = -80) {
    const chunks = [];
    const ctx = new AudioContext();
    const analyser = ctx.createAnalyser();
    const streamNode = ctx.createMediaStreamSource(stream);
    streamNode.connect(analyser);
    analyser.minDecibels = min_decibels;
  
    //const mediaRecorder = new MediaRecorder(stream);
    //mediaRecorder.start();

    const data = new Uint8Array(analyser.frequencyBinCount); // will hold our data
    let silence_start = performance.now();
    let triggered = false; // Silent by default
  
    let loopid;

    function loop(time) {
      loopid = requestAnimationFrame(loop); // we'll loop every 60th of a second to check
      console.log(triggered);
      analyser.getByteFrequencyData(data); // get current data
      if (data.some(v => v)) { // if there is data above the given db limit
        if(!triggered){
          triggered = true; //Speaking
          onSoundStart();
          }
        silence_start = time; // set it to now
      }
      if (triggered && time - silence_start > silence_delay) {
        //mediaRecorder.stop();
        recognition.stop();
        console.log("Stopped listening");
        triggered = false;
        cancelAnimationFrame(loopid);
        onSoundEnd();
      }
    }

    /*setTimeout(() => {
        mediaRecorder.stop();
        console.log("THIS IS STOPPING");
        console.log(chunks);
    }, 2000);*/
    /*mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
        console.log(chunks);
    }*/
    loop();
}

window.addEventListener("DOMContentLoaded", (event) => {
    window.utterances = [];
    const startButton = document.getElementById('startButton');
    const log = document.getElementById('log');
    let exchanges = 0;

    const onSilence = () => {
        log.textContent += 'silence\n';
    };

    const onSpeak = () => {
        log.textContent += 'speaking\n';
    };

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = 'en-US';
    let hasResults = false;
    recognition.onstart = () => {
        hasResults = false;
        console.log("starting listening, speak in microphone");
        navigator.mediaDevices.getUserMedia({
            audio: true
        })
        .then(stream => {
            detectSilence(stream, recognition, onSilence, onSpeak, 500, -60);
            // do something else with the stream
        }).catch(e=>log.textContent=e);
    }
    /*recognition.onspeechend = () => {
        console.log("stopped listening");
        recognition.stop();
    };*/

    const synth = window.speechSynthesis;
    const voices = synth.getVoices();
    const THEvoice = voices[0];
    for (const v of voices)
        if (v.default)
            THEvoice = v;

    const AI_starter = "Hi! I'm the personal AI assistant for my user. How can I help you?";

    const createUtterance = (ai) => {
        const utterThis = new SpeechSynthesisUtterance(ai);
        utterThis.voice = THEvoice;
        utterThis.onstart = () => {
            console.log("I have started");
        }
    
        utterThis.onend = () => {
            console.log("Finished speaking");
            console.log("Currently finished " + exchanges + " exchanges");
            if (exchanges < 3) {   
                setTimeout(() => {
                    recognition.start();
                }, 500);
            }
        }

        utterances.push(utterThis);
        return utterThis;
    }

    const askAI = (vocalInput) => {
        exchanges += 1;
        fetch('http://localhost:3000/classify', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({vocalInput, exchanges})
        })
        .then(response => response.json())  
        .then(json => {
            console.log("The AI assistant responds:");
            console.log(json);
            const continue_utterance = createUtterance(json.response);
            setTimeout(() => {
                synth.speak(continue_utterance);
            }, 500);
        })
    };

    recognition.onresult = (e) => {
        hasResults = true;
        console.log("Results:");
        let vocalInput = e.results[0][0].transcript;
        console.log(vocalInput);
        //Call Python API to fetch response
        askAI(vocalInput);
    };

    /*recognition.onnomatch = (e) => {
        console.log("NO RESULTS");
        let vocalInput = "I don't know";
        askAI(vocalInput);
    }

    recognition.onerror = (e) => {
        console.log("ERROR");
        let vocalInput = "I don't know";
        askAI(vocalInput);
    }*/


    recognition.onend = (e) => {
        console.log("END");
        if(!hasResults) {
            let vocalInput = "I don't know";
            askAI(vocalInput);
        }
    }

    startButton.addEventListener('click', () => {
        startButton.disabled = true;
        const starting_utterance = createUtterance(AI_starter);
        synth.speak(starting_utterance);
        console.log("Having spoken");
    });
});
  