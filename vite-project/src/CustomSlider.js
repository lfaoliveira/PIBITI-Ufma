import videojs from 'video.js';

const Slider = videojs.getComponent("Slider");
// Extend the Slider class
export default class CustomSeekBar extends Slider {
  constructor(player, options) {
    super(player, options);
  }

  // Create the slider element
  createEl() {
    return super.createEl(
      "div",
      {
        className: "vjs-custom-slider",
      },
      {
        "aria-label": "Custom Seek Bar",
      }
    );
  }

  // Calculate the position of the slider
  handleMouseMove(event) {
    const percent = this.calculateDistance(event);
    const newTime = percent * this.player_.duration();
    this.player_.currentTime(newTime); // Set the new playback time
  }

  // Update the slider position based on the current playback time
  update() {
    const percent = this.player_.currentTime() / this.player_.duration();
    this.el_.style.width = `${percent * 100}%`;
  }
}

// Register the component
videojs.registerComponent("CustomSeekBar", CustomSeekBar);