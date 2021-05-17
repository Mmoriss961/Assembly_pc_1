   $(document).ready(function(){

        $("a").on('click',function (){
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=" + this.hash.slice(1) + "]');
        $(".main_menu .menu li > a[href*='#']")
        if (target.length) {
          $("html, body").animate({
            scrollTop: target.offset().top - 100
          }, 1000);
          return false;
        }
      }
    });
         if(window.location.hash){
            scroll(0,0);
            setTimeout(function (){
                scroll(0,0);
            },1);
        }
        if(window.location.hash ){
            $("html,body").animate({
                scrollTop: $(window.location.hash).offset().top - 100
            },1000);
            history.pushState('', document.title, window.location.pathname+window.location.search);
        }

    });


