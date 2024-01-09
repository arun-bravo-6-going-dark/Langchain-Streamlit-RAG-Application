# Define multiple credentials with additional details
credentials = {
    "user1@example.com": {"password": "password1", "name": "Alice", "age": 25, "gender": "Female", "membership_level": "Gold", "joining_year": 2019, "profile_picture": "alice.jpeg"},
    "user2@example.com": {"password": "password2", "name": "Bob", "age": 30, "gender": "Male", "membership_level": "Bronze", "joining_year": 2024, "profile_picture": "bob.jpeg"}, 
    "user3@example.com": {"password": "password3", "name": "Aladdin", "age": 28, "gender": "Male", "membership_level": "Diamond", "joining_year": 2014, "profile_picture": "aladdin.jpeg"},
    # Add more users as needed
}

# JavaScript to manage the scroll position
scroll_js = """
<script>
function maintainScrollPosition(){
    var container = document.querySelector("[data-testid='column']>div>div>div>div>div");
    var scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        container.scrollTop = scrollPosition;
    }
    container.addEventListener('scroll', function() {
        localStorage.setItem('scrollPosition', container.scrollTop);
    });
}
// Call the function when the page loads
setTimeout(maintainScrollPosition, 500);
</script>
"""