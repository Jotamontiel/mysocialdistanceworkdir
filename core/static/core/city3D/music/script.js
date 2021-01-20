$(document).ready(function() {
    var music = document.getElementById("music");
    var play_music_button = document.getElementById("play_music_button");

    function playAudio() {
        if (music.paused) {
            music.play();
            play_music_button.className = 'button button2 pause';
        } else {
            music.pause();
            play_music_button.className = 'button button2 play';
        }
        music.addEventListener('ended',function() {
            play_music_button.className = 'button button2 play';
        });
    }
    play_music_button.addEventListener("click", playAudio);
});