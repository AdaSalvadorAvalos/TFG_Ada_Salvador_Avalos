function NotesIterator()
{
    this.m_notes_producer = null;
    this.m_pos = 0;

    this.First = function()
    {
            this.m_pos = 0;
    }

    this.End = function()
    {

      //  alert("end" + this.m_pos + " " + this.m_notes_producer.elements.elements.length )
        return (this.m_pos >= this.m_notes_producer.elements.elements.length);
    }

    this.Get = function()
    {
       return  this.m_notes_producer.elements.elements[this.m_pos];
    }

    this.Next = function()
    {
       return  this.m_pos++;
    }

}

function NotesProducer()
{

    this.elements = null;
    this.m_seek_pos = -1;
    this.m_seek_measure= -1;

    this.time_signature = "";
    this.key_signature  = 0;


    this.GetIterator = function()
    {
        var iterator = new NotesIterator();
        iterator.m_notes_producer = this;
        return iterator;
    }


    // *********************

    this.GetKeyVexflow = function(key_signature)
    {
        if(key_signature==0) return "C";
        if(key_signature==6) return "F#";
        if(key_signature==5) return "B";
        if(key_signature==4) return "E";
        if(key_signature==3) return "A";
        if(key_signature==2) return "D";
        if(key_signature==1) return "G";
        if(key_signature==-6) return "Gb";
        if(key_signature==-5) return "Db";
        if(key_signature==-4) return "Ab";
        if(key_signature==-3) return "Eb";
        if(key_signature==-2) return "Bb";
        if(key_signature==-1) return "F";
        

    }

    this.Deserialize = function(str_json) {
        this.elements = JSON.parse(str_json);  
        this.time_signature =  this.elements.time_signature;
        this.key_signature = this.GetKeyVexflow(this.elements.key_signature);
    };


    this.GetMeasuresCount = function()
    {
        var old_measure= null;
        var count = 0 ;
        var i= 0;
       while(i < this.elements.elements.length){
            var measure = this.elements.elements[i];
            if(measure.m != old_measure){
                count++;
                old_measure=measure.m;
            }
            i++;
       }
        return count;

    }


    this.SeekMeasure = function(pmeasure)
    {
        var i=0;

        this.m_seek_measure = pmeasure;
        while(i < this.elements.elements.length){
            var measure = this.elements.elements[i];
            if(measure.m == pmeasure){
                this.m_seek_pos = i;
                break;
            }
            i++;
       }
    }



    this.End = function()
    {
       var result = false;
        

        if((this.m_seek_pos>=this.elements.elements.length) || 
            (this.elements.elements[this.m_seek_pos].m != this.m_seek_measure)){
             
                result = true;
        }


        return result;
    }

    this.Get = function()
    {
       var note = null;
        
       if(this.m_seek_pos<this.elements.elements.length){
            note = this.elements.elements[this.m_seek_pos];

       }

        return note;
    }


    // After seekMeasure
    this.Next = function()
    {
         
       
            
        this.m_seek_pos++;
        


       
    }



}