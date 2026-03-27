class AudioAgent {
    constructor() {
        this.voices = {
            'male_host': { name: 'James', pitch: 1.0, rate: 1.0 },
            'female_host': { name: 'Sarah', pitch: 1.1, rate: 1.0 },
            'male_guest': { name: 'Michael', pitch: 0.95, rate: 0.98 },
            'female_guest': { name: 'Emma', pitch: 1.05, rate: 1.02 }
        };
    }
    
    async generateSpeech(text, voiceId) {
        return new Promise((resolve, reject) => {
            if (!window.speechSynthesis) {
                reject(new Error('Speech synthesis not supported'));
                return;
            }
            
            const voice = this.voices[voiceId];
            if (!voice) {
                reject(new Error(`Voice ${voiceId} not found`));
                return;
            }
            
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            const voices = window.speechSynthesis.getVoices();
            const matchingVoice = voices.find(v => v.name.toLowerCase().includes(voice.name.toLowerCase()));
            
            if (matchingVoice) utterance.voice = matchingVoice;
            utterance.pitch = voice.pitch;
            utterance.rate = voice.rate;
            utterance.lang = 'en-US';
            
            utterance.onend = () => resolve();
            utterance.onerror = (error) => reject(error);
            
            window.speechSynthesis.speak(utterance);
        });
    }
    
    async generateScript(content, topic) {
        return [
            { speaker: 'host', text: `Welcome everyone to this episode! Today we're diving deep into "${topic}".` },
            { speaker: 'guest', text: `Thanks for having me! I'm excited to explore ${topic} with all of you.` },
            { speaker: 'host', text: `Let's start with the basics. ${content.substring(0, 150)}...` },
            { speaker: 'guest', text: `That's a great point. In my experience, this is crucial for understanding the bigger picture.` },
            { speaker: 'host', text: `What would you say is the most important takeaway for our listeners?` },
            { speaker: 'guest', text: `I think the key is to stay curious and always be willing to learn.` },
            { speaker: 'host', text: `Wonderful insight! Thank you for joining us today.` },
            { speaker: 'guest', text: `Thank you for having me! It's been a pleasure.` },
            { speaker: 'host', text: `Thanks for listening! Don't forget to subscribe for more amazing content.` }
        ];
    }
    
    stopAllSpeech() {
        if (window.speechSynthesis) window.speechSynthesis.cancel();
    }
}

window.AudioAgent = AudioAgent;