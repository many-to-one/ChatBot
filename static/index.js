function getCookie(name) {
    const cookieArr = document.cookie.split(";"); // Split cookies into an array

    for (let cookie of cookieArr) {
        const cookiePair = cookie.trim().split("="); // Split the key-value pair

        if (cookiePair[0] === name) {
            return cookiePair[1]; // Return the cookie value
        }
    }

    return null; // Return null if the cookie isn't found
}

const access_token = getCookie("access_token");

async function sendMessage(event) {
    event.preventDefault(); // Prevent page reload

    var textArea = document.getElementById("textArea");
    var chatWindow = document.getElementById("chatWindow");
    var userMessage = textArea.value.trim();
    var spinner = document.getElementById("spinner");

    // Show spinner while waiting for response
    spinner.style.display = "block";
    chatWindow.style.opacity = "0.8";

    if (!userMessage) return; // Ignore empty messages

    // Add user message to chat window
    var userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("chat-message", "user-message");
    userMessageDiv.innerText = userMessage;
    chatWindow.appendChild(userMessageDiv);

    // Clear textarea
    textArea.value = "";

    var formData = new FormData();
    formData.append('user_input', userMessage);

    console.log("Access Token:", access_token);

    // Send request to FastAPI
    const resp = await axios.post("http://127.0.0.1:8006/ai_chat/chat", 
        // {
        //     headers: {
        //         "Content-Type": "application/x-www-form-urlencoded",
        //         "Authorization": `Bearer ${access_token}`
        //     },
        //     withCredentials: true
        // },
            formData,
        )
    // console.log('axios response ---', resp);
        .then(response => {
            console.log('axios response ---', response);

            // Hide spinner once response is received
            spinner.style.display = "none";
            chatWindow.style.opacity = "1";

            var assistantMessage = response.data.answer;

            // Add assistant response to chat window
            var assistantMessageDiv = document.createElement("div");
            assistantMessageDiv.classList.add("chat-message", "assistant-message");
            assistantMessageDiv.innerHTML = assistantMessage; // Use innerHTML to support formatting
            chatWindow.appendChild(assistantMessageDiv);

            // Trigger Prism.js syntax highlighting
            // Prism.highlightAll();

            // Scroll to latest message
            chatWindow.scrollTop = chatWindow.scrollHeight;
        })
        .catch(error => {
            console.error('access_token ??? ---', access_token);
            console.error("Error:", error, access_token);
        });
}



async function imgGenerate(event) {
    event.preventDefault(); // Prevent page reload

    var textArea = document.getElementById("textArea");
    var chatWindow = document.getElementById("chatWindow");
    var userMessage = textArea.value.trim();
    var spinner = document.getElementById("spinner");

    // Show spinner while waiting for response
    spinner.style.display = "block";
    chatWindow.style.opacity = "0.8";

    if (!userMessage) return; // Ignore empty messages

    // Add user message to chat window
    var userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("chat-message", "user-message");
    userMessageDiv.innerText = userMessage;
    chatWindow.appendChild(userMessageDiv);

    // Clear textarea
    textArea.value = "";

    var formData = new FormData();
    formData.append('user_input', userMessage);

    await axios.post("/image-generate", 
        {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": `Bearer ${access_token}`
            },
            withCredentials: true
        },
        formData)
        .then(response => {
            console.log('axios response ---', response);

            // Hide spinner once response is received
            spinner.style.display = "none";
            chatWindow.style.opacity = "1";

            var image_bytes = response.data
            var assistantMessageDiv = document.createElement("div");
            var imgElem = document.createElement("img");
            imgElem.src = `data:image/jpeg;base64,${image_bytes}`;
            imgElem.className = 'resp-img';
            imgElem.width = "200px";
            imgElem.height = "200px";
            assistantMessageDiv.appendChild(imgElem)
            chatWindow.appendChild(imgElem);
        }) 
        .catch(error => {
            console.error("Error:", error);
            window.location.reload()
        });
}


async function imgToImg(event) {
    event.preventDefault(); // Prevent page reload

    var textArea = document.getElementById("imgToImgArea");
    var chatWindow = document.getElementById("chatWindow");
    var userMessage = textArea.value.trim();
    var spinner = document.getElementById("spinner");

    // Show spinner while waiting for response
    spinner.style.display = "block";
    chatWindow.style.opacity = "0.8";

    if (!userMessage) return; // Ignore empty messages

    // Add user message to chat window
    var userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("chat-message", "user-message");
    userMessageDiv.innerText = userMessage;
    chatWindow.appendChild(userMessageDiv);

    // Clear textarea
    textArea.value = "";

    var formData = new FormData();
    var fileInput = document.getElementById("image");
    formData.append('file', fileInput.files[0]); // Add the uploaded file
    formData.append('prompt', userMessage);

    await axios.post("/image-to-image", formData)
        .then(response => {
            console.log('axios response ---', response);

            // Hide spinner once response is received
            spinner.style.display = "none";
            chatWindow.style.opacity = "1";

            var image_bytes = response.data
            var assistantMessageDiv = document.createElement("div");
            var imgElem = document.createElement("img");
            imgElem.src = `data:image/jpeg;base64,${image_bytes}`;
            imgElem.className = 'resp-img';
            assistantMessageDiv.appendChild(imgElem)
            chatWindow.appendChild(imgElem);
        }) 
        .catch(error => {
            console.error("Error:", error);
            // window.location.reload()
        });
}
