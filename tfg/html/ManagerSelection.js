function ManagerSelection()
{
    this.note_selection = [];
    this.m_score_manager = null;

    this.GetSelection = function()
    {
       // return JSON.stringify(this.note_selection);
       return  this.note_selection;
    }

    this.DrawLinePosition = function(x,y1,y2)
    {
        var context = g_score_manager.context;

        var old_line = document.getElementById('vertical-line');
        if(old_line!=null){
            context.svg.removeChild(old_line);
        }

        /*
        // Draw the new vertical line
        context.beginPath();
        context.moveTo(x, y1);
        context.lineTo(x, y2);
        context.setAttribute('id', 'vertical-line');
        context.setLineWidth(1);
        context.setStrokeStyle('red');
        context.stroke();
        */

        var new_line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        new_line.setAttribute('id', 'vertical-line');
        new_line.setAttribute('x1', x);
        new_line.setAttribute('y1', y1);
        new_line.setAttribute('x2', x);
        new_line.setAttribute('y2', y2);
        new_line.setAttribute('stroke', 'red');
        new_line.setAttribute('stroke-width', '1');
    
        // Append the new line to the SVG context
        context.svg.appendChild(new_line);

    }

    this.changeColorSelect = function(id){

        var notehead = $('[data-internal-id="' + id + '"]');
       


       if("" + notehead != "undefined"){

          
            //alert(notehead[0].outerHTML);
            notehead.attr('fill', 'red');
           
       }

      
      //  alert(notehead.html());
       // notehead.setAttribute('fill', 'red');
    }

    this.changeColorUnselect = function(id){
        
        var notehead = $('[data-internal-id="' + id + '"]');
        if("" + notehead != "undefined"){
      
       // notehead.setAttribute('fill', 'black');
        notehead.attr('fill', 'black');
        }
       
    }
    
    this.AddNote = function(stringToAdd)
    {   

      
       try{
            if(!isCtrlPressed){
            
                    if(this.Exists(stringToAdd)){
                    
                        this.UnselectAll();
                    
                    }
                    else{
                        this.UnselectAll();
                        this.note_selection.push(stringToAdd);
                        this.changeColorSelect(stringToAdd) ;  
                    }
                    
            }
            else{
                    //alert(stringToAdd);
                    if(this.Exists(stringToAdd)==false){
                            //alert("Add");
                            this.note_selection.push(stringToAdd);
                            this.changeColorSelect(stringToAdd);   
                    }
                    else
                    {
                            //alert("Remove");
                            this.RemoveNote(stringToAdd);
                            this.changeColorUnselect(stringToAdd);
                    }
            }
        }
        catch(e)
        {
            alert(e);
        }
    }

    this.RemoveNote = function(stringtoRemove)
    {
        let index = this.note_selection.indexOf(stringtoRemove);
        if(index !== -1){
            this.note_selection.splice(index, 1);
        }

    }

    this.Exists = function(stringtoCheck)
    {
        var result = false;
        for (var i = 0; i < this.note_selection.length; i++) {

         //   alert(this.note_selection[i] + " " +stringtoCheck);
            if (this.note_selection[i] == stringtoCheck) {

                result = true;
                break;
            }
        }

      // alert(result);
        return result;
    }

  

    this.UnselectAll = function()
    {
   
        for (let i = 0; i < this.note_selection.length; i++) {
            this.changeColorUnselect(this.note_selection[i]);
          }


        this.note_selection = [];
    }

    this.SelectAll = function()
    { 
        this.note_selection = [];

        try{
            var iterator = this.m_score_manager.m_notes_producer.GetIterator();

            iterator.First();
            while(!iterator.End()){
            
            var  note = iterator.Get();



                this.note_selection.push(note.id);
                this.changeColorSelect(note.id);




                iterator.Next();

            }
        }
        catch(e)
        {
            alert(e);
        }
    }


}