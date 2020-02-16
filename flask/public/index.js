function startImageUpdate() {
    const UPDATE_TIME = 100;

    async function changeImage() {
        const emotions = ["joy", "surprise", "angry", "sorrow"];

        var emotion_call = await fetch("/api/emotion");

        let targetEmotion = "joy";

        if (emotion_call.ok) {
            var emo = await emotion_call.json();
            targetEmotion = emo.emotion;
        }

        for (let emotion of emotions) {
            if (emotion !== targetEmotion) {
                document.querySelector(`#${emotion}`).className = "hidden";
            }
        }

        document.querySelector(`#${targetEmotion}`).className = "target_emotion";
    }

    changeImage();

    setInterval(changeImage, UPDATE_TIME);
}

