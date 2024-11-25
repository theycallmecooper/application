document.addEventListener("DOMContentLoaded", () => {
    const postIt = document.getElementById("post-it");
  
    // Remove the post-it note after the animation is complete
    postIt.addEventListener("animationend", () => {
      postIt.style.display = "none";
    });
  });

  // Moving gradient background
let gradientStep = 0;

function animateGradient() {
    gradientStep += 2; // Adjust speed by changing this value
    const color1 = `hsl(${Math.sin(gradientStep) * 360}, 70%, 50%)`;
    const color2 = `hsl(${Math.cos(gradientStep + Math.PI) * 360}, 70%, 50%)`;

    document.body.style.background = `linear-gradient(320deg, ${color1}, ${color2})`;
    requestAnimationFrame(animateGradient);
}

document.addEventListener("DOMContentLoaded", () => {
    animateGradient();

    // Post-it note animation
    const postIt = document.getElementById("post-it");
    if (postIt) {
        postIt.addEventListener("animationend", () => {
            postIt.style.display = "none";
        });
    }
});