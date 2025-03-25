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

document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const access_token = getCookie("access_token");

    try {
        const response = await axios.post("/auth/login", {
            username: username,
            password: password
        }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": `Bearer ${access_token}`
            }
        });

        if (response.status === 200) {
            const data = response.data; // Assuming a TokenResponse is returned
            console.log("Login successful:", data);

            // Redirect to the desired page after login
            window.location.href = "/";
        } 
    } catch (err) {
        if (err.response && err.response.data) {
            document.getElementById("error-message").textContent = err.response.data.detail;
        } else {
            document.getElementById("error-message").textContent = "An unexpected error occurred.";
        }
        document.getElementById("error-message").style.display = "block";
        console.error("Error during login:", err);
    }
});
