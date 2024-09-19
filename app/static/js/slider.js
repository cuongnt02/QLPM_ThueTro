function sliderValue() {
    slider = document.querySelector("#rangeInput");
    sliderValue = document.querySelector("#sliderValue");
    slider.step = 0.5

    slider.onchange = function() {
        sliderValue.textContent = slider.value;
    };
}

sliderValue();

