/*A quick port of the Reveal.js framework into codepen so that I can house my presentations for the classes I teach.

I'm combining the essentials of Hakim El Hattab's excellent Reveal.js presentation framework. (https://github.com/hakimel/reveal.js) with Jack Doyle's GSAP "greensock" animation platform (https://www.greensock.com/) to see if I can rival Keynote's slidey goodness.*/

Reveal.initialize({
  slideNumber: true,
  history:true,
});

/*Quick use of the TweenMax with Reveal.js simply add the Reveal "data-state" attribute to the section (slide) you want to add animation to and with the Reveal.addEventListener API call you wrap you Tween in an anonymous function.  HINT: Using the ".from" method of TweenMax is perfect for building your slide into view
*/
Reveal.addEventListener('traitsSlide', function(){
  TweenMax.staggerFrom('#list li', 0.5, {delay:1, scale:0, alpha:0, ease:'Back.easeOut'}, 0.25);
});

Reveal.addEventListener('adAgeSlide', function(){
  TweenMax.from('#title', .7, {delay:2, scale:4, alpha:0, ease:'Power1.easeOut'});
});