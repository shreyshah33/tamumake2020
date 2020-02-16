async function startImageUpdate() {
    const UPDATE_TIME = 333;
    const emotions = ["joy", "surprise", "angry", "sorrow"];
    let lastVideo = false;
    let lastHash = '';
    let lastShouldRemind = false;

    function updateEmotion(targetEmotion) {
        for (let emotion of emotions) {
            if (emotion !== targetEmotion) {
                document.querySelector(`#${emotion}`).className = "hidden";
            }
        }

        if(targetEmotion != null){
            document.querySelector(`#${targetEmotion}`).className = "target_emotion";
        }
    }

    function displayVideo(display){
        document.querySelector('#video').className = display ? '' : 'hidden';
    }

    function displayPillAlert(display){
        document.querySelector('#pillnote').className = display ? '' : 'hidden';
    }

    function showShopping(list){
        console.log(list);
        const listPadder = document.querySelector('#shopholder');
        const selector = document.querySelector('#shoppingList');
        
        if(list.length > 0){
            listPadder.className = '';
            selector.innerHTML = '';
            for (let item of list){
                let listItem = document.createElement('li');
                listItem.appendChild(document.createTextNode(item));
                selector.appendChild(listItem);
            }
        }else{
            listPadder.className = 'hidden';
        }
    }

    async function updateGUI() {
        

        let gui = await fetch("/api/guiUpdate");

        let targetEmotion = "joy";
        let video = false;

        let orders = [];
    
        let shouldRemind = false;
        
        if (gui.ok) {
            gui = await gui.json();
            targetEmotion = gui.emotion;
            raw_list = gui.order;

            for(let i = 0; i < raw_list.length; i++){
                if(i % 2 == 0){
                    orders.push(raw_list[i])
                }else{
                    orders[orders.length - 1] = `${raw_list[i]} - ${orders[orders.length - 1]}`
                }
            }

            shouldRemind = !gui.pills;
            video = gui.start;
        }

        if(lastVideo != video){
            if(!video){
                updateEmotion(null);
            }

            displayVideo(video);
        }

        if(video){
            updateEmotion(targetEmotion);
        }

        if(lastHash !== JSON.stringify(orders)){
            showShopping(orders);
        }

        if(shouldRemind !== lastShouldRemind){
            displayPillAlert(shouldRemind);
        }

        lastVideo = video;

        lastHash = JSON.stringify(orders);
        lastShouldRemind = shouldRemind;
    }

    updateEmotion(null);
    displayVideo(false);
    displayPillAlert(false);

    setInterval(updateGUI, UPDATE_TIME);


    const darksky = await fetch('/api/weather');

    if(darksky.ok){
        const weather = await darksky.json();

        document.querySelector('#condition').innerHTML = weather.currently.summary;
        document.querySelector('#temp').innerHTML = weather.currently.temperature;
    }
}

