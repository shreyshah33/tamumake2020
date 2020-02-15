
function startImageUpdate(){
    const UPDATE_TIME = 1000;

    async function changeImage() {
        const emotions = ['joy', 'suprise', 'angry', 'sorrow'];

        const emotion_call = await fetch('/api/emotion')

        let targetEmotion = 'joy';

        if(emotion_call.ok){
            targetEmotion = (await emotion_call.json()).emotion;
        }

        for (let emotion of emotions) {
            if(emotion !== targetEmotion){
                document.querySelector(`#${emotion}`).className = 'hide_emotion';
            }
        }

        document.querySelector(`#${targetEmotion}`).className = 'target_emotion';
    }

    changeImage();

    setInterval(changeImage, UPDATE_TIME);
}