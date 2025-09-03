function PythonCom()
{
    this.m_control = null;    
    this.LoadFile = function()
    {
        var obj = {
                        id:"LoadFile"

                    };   

        this.send_msg_to_python(obj);


    }

    this.MirrorEffect = function()
    {
        var obj = {
                        id:"MirrorEffect"

                    };   

        this.send_msg_to_python(obj);


    }

    this.Play = function()
    {
        var obj = {
                        id:"Play"

                    };   

        this.send_msg_to_python(obj);


    }

    this.Stop = function()
    {
        var obj = {
                        id:"Stop"

                    };   

        this.send_msg_to_python(obj);


    }

    this.Save = function()
    {
        var obj = {
                        id:"Save"

                    };   

        this.send_msg_to_python(obj);


    }


    this.SaveAs = function()
    {
        var obj = {
                        id:"SaveAs"

                    };   

        this.send_msg_to_python(obj);


    }

    this.SelectPlugin = function(p_name)
    {

        var obj = {
            id:"SelectPlugin",
            name: p_name
        };   

        this.send_msg_to_python(obj);
    }

    this.change_time_signature_at_start = function(p_new_time_sig)
    {

        var obj = {
            id:"change_time_signature_at_start",
            new_time_sig: p_new_time_sig
        };   

        this.send_msg_to_python(obj);
    }

    this.change_key_signature_at_start = function(p_new_key_sig)
    {

        var obj = {
            id:"change_key_signature_at_start",
            new_key_sig: p_new_key_sig
        };   

        this.send_msg_to_python(obj);
    }


    this.IntervalChange = function(p_num,p_selection)
    {

        var obj = {
            id:"IntervalChange",
            num: p_num,
            selection: p_selection
        };   

        this.send_msg_to_python(obj);
    }


    this.RemoveNotes = function(p_selection)
    {

        var obj = {
            id:"RemoveNotes",
            selection: p_selection
        };   

        this.send_msg_to_python(obj);
    }
   
    this.AddNote = function(p_measure_id,p_x,p_y,p_width,p_height,p_note,p_staff,p_duration,p_octave, p_accidental)
    {

        var obj = {
            id:"AddNote",
            measure_id: p_measure_id,
            x: p_x,
            y: p_y,
            width: p_width,
            height: p_height,
            note: p_note,
            staff: p_staff,
            duration: p_duration,
            octave: p_octave,
            accidental: p_accidental
        };   

        this.send_msg_to_python(obj);
    }


    this.send_msg_to_python = function(obj){

        var msg = JSON.stringify(obj);
        var webChannel = new QWebChannel(qt.webChannelTransport, function(channel) {
            var pyBridge = channel.objects.pyBridge;
            pyBridge.handleMessage(msg);
           
        });
    }

    this.HandleMessage = function(ope_id,param1,param2,param3){

            
            if(ope_id=="OnLoadFile"){
              
                this.m_control.OnLoadFile(param1);
            }
            else if(ope_id=="alert"){
                alert(param1);
            }
    }

}