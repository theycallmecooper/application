document.addEventListener("DOMContentLoaded", () => {
    const postIt = document.getElementById("post-it");
  
    // Remove the post-it note after the animation is complete
    postIt.addEventListener("animationend", () => {
      postIt.style.display = "none";
    });
  });