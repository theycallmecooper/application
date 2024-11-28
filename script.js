document.addEventListener("DOMContentLoaded", () => {
    const postIt = document.getElementById("post-it");
  
    // Remove the post-it note after the animation is complete
    postIt.addEventListener("animationend", () => {
      postIt.style.display = "none";
    });

    const gradientBackground = document.querySelector('.gradient-background');
    let gradientStep = 0;
    const gradientSpeed = 0.005; // Adjust speed as needed

    function animateGradient() {
        gradientStep += gradientSpeed;
        if (gradientStep >= 1) {
            gradientStep = 0;
        }

        const r = Math.round(137 * (1 - gradientStep) + 34 * gradientStep);
        const g = Math.round(51 * (1 - gradientStep) + 19 * gradientStep);
        const b = Math.round(235 * (1 - gradientStep) + 151 * gradientStep);

        const color1 = `rgb(${r}, ${g}, ${b})`;
        const color2 = `rgb(34, 19, 151)`; // Dark blue

        gradientBackground.style.background = `linear-gradient(90deg, ${color1}, ${color2})`;

        requestAnimationFrame(animateGradient);
    }

    animateGradient();
});

document.addEventListener("DOMContentLoaded", () => {
    const postIt = document.getElementById("post-it");
    if (postIt) {
        postIt.addEventListener("animationend", () => {
            postIt.style.display = "none";
        });
    }
});
