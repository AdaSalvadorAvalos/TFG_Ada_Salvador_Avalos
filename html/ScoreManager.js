function ScoreManager()
{
    this.renderer = null;
    this.context = null;
    this.m_layout_manager = null;

    this.svg_container = null;

    this.voices = [];

    this.m_notes_producer = null;
    
    this.Start = function(div,width,height)
    {

        this.svg_container = div;
        this.renderer = new Renderer(div, Renderer.Backends.SVG);

        // Configure the rendering context
        this.renderer.resize(width, height);
        this.context =  this.renderer.getContext();
    }

    this.Resize = function()
    {
        // Measure the bounding box of the rendered SVG
        const bbox = this.svg_container.querySelector('svg').getBBox();

        // Resize the renderer to fit the content
       // this.renderer.resize(bbox.width, bbox.height + 50);
       this.renderer.resize(1415, bbox.height + 50);


      //  alert("Resize" + bbox.width);
        
        // Clear the context and redraw the stave with the resized renderer
        /*
        this.context.clear();
        stave.setWidth(bbox.width);
        stave.draw();
        voice.draw(context, stave);
        */

    }


    this.RenderData = function(str_json)
    {

        this.measures = [];
        var t_producer = new NotesProducer();
        t_producer.Deserialize(str_json);

        this.m_notes_producer = t_producer;


        var context = this.context;
       

        var y = 10;
        var distance_btw_hands = 100;
        var size_measure = 350;

        var measures1 = [];
        var measures2 = [];
        var x = 20;

        var measures_count = t_producer.GetMeasuresCount();

        var measure_position = 1;
        t_producer.SeekMeasure(measure_position);

        var measures_per_file = 4; // 4

        for (var i = 0; i < Math.ceil(measures_count / measures_per_file); i++) {
        x=20;

        for (var j = 0; j < measures_per_file; j++) {
            var stave = new Stave(x, y, size_measure);
            var stavebass = new Stave(x, distance_btw_hands + y, size_measure);
            
            stave.measure_id = measure_position;
            stave.staff = "treble";
            stavebass.measure_id = measure_position;
            stavebass.staff = "bass";

            this.measures.push(stave);
            this.measures.push(stavebass);

            if(i==0 && j==0){
            // var stave = new Stave(x, y, size_measure);
            // var stavebass = new Stave(x, distance_btw_hands + y, size_measure);
            
                // Add clef and time signature
                stave.addClef("treble").addTimeSignature(t_producer.time_signature).addKeySignature(t_producer.key_signature);
                stave.setContext(context).draw();
                stavebass.addClef("bass").addTimeSignature(t_producer.time_signature).addKeySignature(t_producer.key_signature);
                stavebass.setContext(context).draw();
                /*
                stave.addClef("treble").addTimeSignature("4/4").addKeySignature("Db");
                stave.setContext(context).draw();
                stavebass.addClef("bass").addTimeSignature("4/4").addKeySignature("Db");
                stavebass.setContext(context).draw();
                */

                var connector_brace = new StaveConnector(stave, stavebass);
            connector_brace.setType(StaveConnector.type.BRACE);
            connector_brace.setContext(context).draw();
        }
        else if(j==0 && i!=0){
                
            stave.addClef("treble").addKeySignature(t_producer.key_signature);
            stave.setContext(context).draw();

            stavebass.addClef("bass").addKeySignature(t_producer.key_signature);
            stavebass.setContext(context).draw();

            var connector_brace = new StaveConnector(stave, stavebass);
            connector_brace.setType(StaveConnector.type.BRACE);
            connector_brace.setContext(context).draw();
            
            }
            else{
            stave.setContext(context).draw();
            stavebass.setContext(context).draw();

            var connector = new StaveConnector(stave, stavebass);
            connector.setType(StaveConnector.type.SINGLE); 
            connector.setContext(context).draw();

            }
        
            var note = null;  
            var notesMeasure1 = [];
            var notesMeasure2 = [];
            var temp = 0;

        // var offsetX = 0;
            while(!t_producer.End()){

            
                note = t_producer.Get();
                temp++;
                
                try{
                var add_accidental = false;
                var accidental_type = "";
                if(note.pitch.indexOf("#")!=-1){
                    var l = note.pitch.substr(0,1);
                    var n = note.pitch.substr(2,1);
                    l = l.toLowerCase();
                    add_accidental = true;
                    accidental_type = "#";
                    var str = l + "#/" + n;

                }
                else if(note.pitch.indexOf("-")!=-1){

                    add_accidental = true;
                    accidental_type = "b";
                    var l = note.pitch.substr(0,1);
                    var n = note.pitch.substr(2,1);
                    l = l.toLowerCase();
                    var str = l + "b/" + n;
                    
                }
                else{
                    var l = note.pitch.substr(0,1);
                    var n = note.pitch.substr(1,1);
                    l = l.toLowerCase();
                    
                    var str = l + "/" + n;

                    /*
                    if(note.v == 1){
                        str = this.TranformToBass(l,n);
                    };
                    */
                }
                
                if(t_producer.key_signature != "C") add_accidental = false;
                
                
                var dur = note.duration;
                

                /*
                if(dur == 0.5){
                    dur = "8";
                }
                else if (dur == 1) {
                    dur = "q";
                } else  if(dur == 2){
                    dur = "h";
                }
                else  if(dur == 3){
                    dur = "hd";
                    
                }
                else {
                    dur = "16";
                }
    */

            dur = this.music21DurationToVexFlow(dur);
                
            
                    // Using regular expression to match a letter followed by a number

    // DEpendiento de la voz añadirlo a un sitio o a otro.
                var new_note;
                var new_noteBAD;
                if(note.v == 2){
                    new_note =  new StaveNote({clef:"treble", keys: [str], duration: dur });
                    notesMeasure1[notesMeasure1.length] =  new_note;

                    new_note.internal_id = note.id;

                    
                    if(add_accidental){
                        new_note.addModifier( new Accidental(accidental_type),0);
                    }


                    new_noteBAD =  new StaveNote({clef:"bass", keys: ["d/3"], duration: dur, type:"r" });
            //     new_noteBAD =  new StaveNote({clef:"treble", duration: dur });
                    
                    new_noteBAD.internal_id = "";
                    
                   
                    
                    notesMeasure2[notesMeasure2.length] =  new_noteBAD;


            //    new_noteBAD.setStyle({ fillStyle: 'rgba(0, 0, 0, 0)', strokeStyle: 'rgba(0, 0, 0, 0)' });

                }
                else{
                    new_note =  new StaveNote({clef:"bass",keys: [str], duration: dur , stem_direction: -1});        
                   
                    if(add_accidental){
                        new_note.addModifier( new Accidental(accidental_type),0);
                    }

                   // alert("En nota:" +  note.id);
                    new_note.internal_id = note.id;
                    notesMeasure2[notesMeasure2.length] =   new_note;

                //    new_noteBAD =  new StaveNote({clef:"bass", duration: dur , stem_direction: -1});        
            
                    new_noteBAD =  new StaveNote({clef:"treble",keys: ["b/4"], duration: dur , stem_direction: -1, type:"r" });        
                   
                   
                    
                    new_noteBAD.internal_id = "";
                    notesMeasure1[notesMeasure1.length] =   new_noteBAD;

                //   new_noteBAD.setStyle({ fillStyle: 'rgba(0, 0, 0, 0)', strokeStyle: 'rgba(0, 0, 0, 0)' });

        
                }

                if(dur=="hd"){
                    var dotModifier = new Dot();

                    // Add the dot modifier to the note
                    new_note.addModifier(dotModifier,0); 
                }

                // offsetX+=  new_note.getXShift() + 40;
                }
                catch(e)
                {
                    //alert(e);
                }
                t_producer.Next();

            }
        
            console.log("Measure " + measure_position + " notes count " + temp);

            measure_position++;
            
            t_producer.SeekMeasure(measure_position);

            /*
            var notesMeasure1 = [
                new StaveNote({ keys: ["c/4"], duration: "q" }),
                new StaveNote({ keys: ["d/4"], duration: "h" }),
                new StaveNote({ keys: ["f/4"], duration: "q" })
            ];
            */


            if(notesMeasure1.length!=0){

                /*
                notesMeasure1.forEach(function(note) {
    note.stem.setVisibility(false); // Ocultar el tallo de la nota
    });
    */

                var voiceMeasure1 = null;
                
                if(notesMeasure1.length!=3){
                voiceMeasure1 = new Voice({ num_beats: notesMeasure1.length, beat_value: 8 }).setMode(1);
                }
                else{
                    voiceMeasure1 = new Voice({ num_beats: notesMeasure1.length, beat_value: 4 }).setMode(1);
                }


                voiceMeasure1.setStrict(false);
                voiceMeasure1.addTickables(notesMeasure1);
                new Formatter().joinVoices([voiceMeasure1]).format([voiceMeasure1], 200);
                measures1.push(stave);
            
                var beams = Beam.generateBeams(notesMeasure1,{
    beam_rests: false, // Establecer en false para dibujar solo las barras sin las notas
    });

                //voiceMeasure1.draw(context, stave);
                 this.drawVoice(voiceMeasure1,context,stave);
             

                beams.forEach(function(beam) {
                beam.setContext(context).draw();
            });
            
            }


            
            /*
            var notesMeasure2 = [
                new StaveNote({ keys: ["c/4"], duration: "q" }),
                new StaveNote({ keys: ["d/4"], duration: "h" }),
                new StaveNote({ keys: ["f/4"], duration: "q" })
            ];
    */
    

            if(notesMeasure2.length!=0){
    /*
            notesMeasure2.forEach(function(note) {
    note.stem.setVisibility(false); // Ocultar el tallo de la nota
    });
    */

                var voiceMeasure2 = null;
                
                if(notesMeasure2.length!=3){
                voiceMeasure2 = new Voice({ num_beats: notesMeasure2.length, beat_value: 8 }).setMode(1);
                }
                else{
                    voiceMeasure2 = new Voice({ num_beats: notesMeasure2.length, beat_value: 4 });
                }
                voiceMeasure2.setStrict(false);

                voiceMeasure2.addTickables(notesMeasure2);
                new Formatter().joinVoices([voiceMeasure2]).format([voiceMeasure2], 200);
                measures2.push(stavebass);

                var beams = Beam.generateBeams(notesMeasure2,{
    beam_rests: false, // Establecer en false para dibujar solo las barras sin las notas
    });
            
                this.drawVoice(voiceMeasure2,context,stavebass);
               // voiceMeasure2.draw(context, stavebass);

                beams.forEach(function(beam) {
                beam.setContext(context).draw();
            });
            }
            

            // ****************************************
            /*
            context.save();

            var beams = Beam.generateBeams(notesMeasure1,{
    beam_rests: false, // Establecer en false para dibujar solo las barras sin las notas
    });

            // Render the beams
            beams.forEach(function(beam) {
                beam.setContext(context).draw();
            });

            beams = Beam.generateBeams(notesMeasure2,{
    beam_rests: false, // Establecer en false para dibujar solo las barras sin las notas
    });

            // Render the beams
            beams.forEach(function(beam) {
                beam.setContext(context).draw();
            });

            context.restore();
            
    */
                x += size_measure; // Adjust the x position for the next stave
        }


        
        // Increment the vertical position for the next set of staves
        y += distance_btw_hands + 200;

        }

      
        // Detect mouse in notes
        this.AddHandles();


        this.svg_container.addEventListener('click', this.clickScore);

        // Test 
       // g_selection_manager.DrawLinePosition(10,0,120);
    }


    this.drawVoice = function(voice,context,stavebass) {
        voice.draw(context, stavebass);
    

        //setTimeout(() => {
          
        // Add custom attributes to notehead SVG elements
        voice.getTickables().forEach(note => {
        note.noteHeads.forEach(notehead => {
          const svgElement = this.svg_container.querySelector("#vf-"+`${notehead.attrs.id}`);
        //  alert("Search #vf-"+`${notehead.attrs.id}` + "->" +  note.internal_id);
          if (svgElement) {
           
            svgElement.setAttribute('data-internal-id', note.internal_id); // assuming attrs.id holds internal_id
          }
        });
      });
      //  }, 1000);
        
    }


    this.ClickInside = function(measure, event)
    {
        const bbox = measure.getBoundingBox();
        if (
            event.offsetX >= bbox.x &&
            event.offsetX <= bbox.x + bbox.w &&
            event.offsetY >= bbox.y &&
            event.offsetY <= bbox.y + bbox.h
          ) {
            return true;
        
        }
        else
        {
            return false;
        }

    }

    // Mouse events
    this.clickScore = function(event)
    {
       // alert(event.offsetX + ","+event.offsetY);
       var i=0;

       for(i=0;i<g_score_manager.measures.length;i++){
            var measure = g_score_manager.measures[i];
            if(g_score_manager.ClickInside(measure,event)){
                const y1 = measure.getYForLine(0); // Top of the measure
                const y2 = measure.getYForLine(4);
                const x =    event.offsetX;
                const bbox = measure.getBoundingBox();
                var measure_id = measure.measure_id;
                var staff = measure.staff;
              //  alert(measure_id);
                g_selection_manager.DrawLinePosition(x,y1,y2);
               // g_control.LastAddNotePosition(measure_id,event.offsetX-bbox.x,event.offsetY-bbox.y,bbox.w,bbox.h,staff);
               g_control.LastAddNotePosition(measure_id,event.offsetX-bbox.x,event.offsetY-y1,bbox.w,y2-y1,staff);
                
               break;   
            }
       }

    }

    this.AddHandles = function()
    {
            // 1. Get the SVG container element.
            const svgContainer = this.svg_container;

            // 2. Add event listeners to all notehead SVG elements.
            svgContainer.querySelectorAll('.vf-notehead').forEach(notehead => {
                notehead.addEventListener('click', function(event) {
                    // When a note is clicked, handle the selection.
                    // 'notehead' is the clicked SVG element representing a note.
                  handleNoteSelection(notehead);
                  // alert("click");
                });
            });

    }

  
    function handleNoteSelection(notehead) {
       
        const internalId = notehead.getAttribute('data-internal-id');
        const Id = notehead.getAttribute('id');

        const svgCode = notehead.outerHTML;

        g_selection_manager.AddNote(internalId);

        /*
       if(!g_selection_manager.Exists(internalId)){
          //  notehead.setAttribute('fill', 'red');
            g_selection_manager.AddNote(internalId);
       }
       else{
          //  notehead.setAttribute('fill', 'black');
            g_selection_manager.RemoveNote(internalId);
       }
*/

     //   alert(`Note selected:\nInternal ID: ${internalId}\nSVG Code:\n${Id}`);
      //  console.log(`Note selected:\nInternal ID: ${internalId}\nSVG Code:\n${svgCode}`);
    }


    this.TranformToBass = function(letter,octave)
    {

        return  letter + "/" + octave;
        var tmp = "";

        var letter = letter.charCodeAt(0) - "a".charCodeAt(0);
        letter = (letter + 5) % 7;
        letter += "a".charCodeAt(0);


        var total_octave = parseInt(octave,10) + 2;
        tmp += String.fromCharCode(letter) +  "/" + total_octave;

        return tmp;
    } 


    this.music21DurationToVexFlow = function(duration) {
  // Map Music21 durations to VexFlow durations
  var durationMap = {
    0.5:"8",// Eighth note
      1: "q",   // Quarter note
      2: "h",   // Half note
      3: "hd",  // Dotted half note
      4: "w",   // Whole note
      0.125: "32",   // Thirty-second note 
      0.25: "16"  // Sixteenth note 
      // Add more mappings as needed
  };

  return durationMap[duration];
}




}