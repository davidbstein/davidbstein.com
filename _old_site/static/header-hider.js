/* see https://github.com/davidbstein/header-hider for source and licence. */!function(){var a=function(){var a=this;if(a.a=0,a.b=window.onscroll,a.c=document.getElementsByTagName("header")[0],void 0==a.c)throw"in order to use the header hider you must have a <header>";a.c.style.transition="margin-top 0.2s ease-out 0s",a.d=a.c.offsetHeight,a.e=!1,a.f=function(){var a=this;a.c.style.marginTop=-a.d,a.e=!0}.bind(a),a.g=function(){var a=this;a.c.style.marginTop=0,a.e=!1}.bind(a),a.g(),window.onscroll=function(){var a=this;a.b&&a.b();var b=window.pageYOffset;b<64||b<a.a?a.g():a.f(),a.a=b}.bind(a)};if(window.onload){var b;window.onload=function(c){b(c),a()}}else window.onload=a}();