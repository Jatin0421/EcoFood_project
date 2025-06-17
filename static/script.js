document.addEventListener("DOMContentLoaded", function () {
    // Signup Form Submission
    document.getElementById("signupForm").addEventListener("submit", function (event) {
        event.preventDefault();
        
        const username = document.getElementById("signupUsername").value.trim();
        const email = document.getElementById("signupEmail").value.trim();
        const password = document.getElementById("signupPassword").value.trim();
        const role = document.getElementById("signupRole").value;

        if (!username || !email || !password) {
            showError("signupForm", "All fields are required!");
            return;
        }

        showLoading("signupForm", true);

        fetch("http://127.0.0.1:5000/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password, role })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            clearForm("signupForm");
            window.location.href = "login.html"; // Redirect to login
        })
        .catch(error => console.error("Signup error:", error))
        .finally(() => showLoading("signupForm", false));
    });

    // Login Form Submission
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const email = document.getElementById("loginEmail").value.trim();
        const password = document.getElementById("loginPassword").value.trim();

        if (!email || !password) {
            showError("loginForm", "Email and password are required!");
            return;
        }

        showLoading("loginForm", true);

        fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.role) {
                alert(`Login successful! Role: ${data.role}`);
                clearForm("loginForm");
                window.location.href = "index.html"; // Redirect to homepage
            } else {
                showError("loginForm", "Invalid credentials!");
            }
        })
        .catch(error => console.error("Login error:", error))
        .finally(() => showLoading("loginForm", false));
    });

    // Function to clear form fields
    function clearForm(formId) {
        document.getElementById(formId).reset();
    }

    // Function to show error messages
    function showError(formId, message) {
        let errorDiv = document.querySelector(`#${formId} .error-message`);
        if (!errorDiv) {
            errorDiv = document.createElement("p");
            errorDiv.className = "error-message";
            document.getElementById(formId).prepend(errorDiv);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = "block";

        setTimeout(() => {
            errorDiv.style.display = "none";
        }, 3000);
    }

    // Function to show loading animation
    function showLoading(formId, isLoading) {
        const form = document.getElementById(formId);
        const button = form.querySelector("button[type='submit']");
        
        if (isLoading) {
            button.innerHTML = "Processing...";
            button.disabled = true;
        } else {
            button.innerHTML = formId === "loginForm" ? "Login" : "Signup";
            button.disabled = false;
        }
    }
    document.addEventListener("DOMContentLoaded", function () {
        // ... existing code ...
    
        // Add event listeners to password toggle icons
        document.querySelectorAll(".toggle-password").forEach(toggleIcon => {
            toggleIcon.addEventListener("click", function () {
                const passwordField = this.previousElementSibling;
                togglePassword(passwordField);
            });
        });
    
        // ... existing code ...
    });
    
    // ====================
    // Password Toggle Function (Place at the Bottom)
    // ====================
    function togglePassword(passwordField) {
        const toggleIcon = passwordField.nextElementSibling;
    
        if (passwordField.type === "password") {
            passwordField.type = "text";  // Show password
            toggleIcon.textContent = "🔓";  // Change icon when visible
        } else {
            passwordField.type = "password";  // Hide password
            toggleIcon.textContent = "👁️";  // Change icon when hidden
        }
    }