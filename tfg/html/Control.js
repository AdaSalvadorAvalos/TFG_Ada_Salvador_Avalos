function Control()
{
    
    this.m_score_manager = null;




    this.LoadFile = function()
    {
        this.m_python_com.LoadFile();

    }

    this.SaveAs = function()
    {
        this.m_python_com.SaveAs();

    }

    this.OnLoadFile = function(json_data)
    {
        g_layout_manager.Start();
        this.m_score_manager.RenderData(json_data);

        this.m_score_manager.Resize();
    }


    this.IntervalChange = function(num)
    {
        this.m_python_com.IntervalChange(num,g_selection_manager.GetSelection());
    }

    this.RemoveNotes = function()
    {
        this.m_python_com.RemoveNotes(g_selection_manager.GetSelection());
    }

    this.Play = function()
    {
        this.m_python_com.Play();

    }

    this.Stop = function()
    {
        this.m_python_com.Stop();

    }

    this.MirrorEffect = function()
    {
        this.m_python_com.MirrorEffect();

    }

    this.Save = function()
    {
        this.m_python_com.Save();

    }

   
    this.LastAddNotePosition = function(measure_id,x,y,width,height,staff)
    {
        
        this.nn_measure_id = measure_id;
        this.nn_x = x;
        this.nn_y = y;
        this.nn_width = width;
        this.nn_height = height;
        this.nn_staff = staff;
        

      //  this.AddNote("q");
    }


    this.AddNote = function(note,duration,octave, accidental)
    {

      
        this.m_python_com.AddNote(this.nn_measure_id,this.nn_x,this.nn_y,this.nn_width,this.nn_height,note, this.nn_staff, duration, octave,accidental);
    }

    this.SelectPlugin = function(name)
    {

      
        this.m_python_com.SelectPlugin(name);
    }


    this.change_time_signature_at_start = function(new_time_sig)
    {

      
        this.m_python_com.change_time_signature_at_start(new_time_sig);
    }

    this.change_key_signature_at_start = function(new_key_sig)
    {

      
        this.m_python_com.change_key_signature_at_start(new_key_sig);
    }



}