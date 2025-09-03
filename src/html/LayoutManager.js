function LayoutManager()
{
    this.m_score_manager = null;


   
    
    this.Start = function()
    {
        $("#vexbox").html("");
        
        var windowHeight = $(window).height();
        var windowWidth = $(window).width();
         
        var div = document.getElementById("vexbox");
       
        //alert(windowWidth +  "," + windowHeight);
        //this.m_score_manager.Start(div,windowWidth,windowHeight);
        this.m_score_manager.Start(div,1415,windowHeight);
        g_score_manager.Resize();
    }

    this.Resize = function()
    {
        
        var windowHeight = $(window).height();
        var windowWidth = $(window).width();

        g_score_manager.Resize();
      
        var scale = windowWidth / 1415;
        $('#containervex').css({'width': windowWidth, 'height': windowHeight-50, 'top':50});
     // $('#vexbox').css({'width': 1415 *scale, 'height': (windowHeight-50) *scale, 'top':50});
        

       
        $('#vexbox').css('transform', 'scale(' + scale + ')');
      
    }

}