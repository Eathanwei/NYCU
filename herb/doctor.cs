using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Inworld;

public class doctor : MonoBehaviour
{
    private bool allinform = false;
    private bool firsec = false;
    [SerializeField] InworldCharacter CurrentCharacter;
    public bool mission = true;
    public MissionControl missionControl;
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("init");
        CurrentCharacter.SendTrigger("init", false);
    }
    private void Update()
    {
        if (Input.GetKey("y"))
        {
            Debug.Log("y");
            ablegetantidote();
        }
        if (Input.GetKey("e"))
        {
            MedicineEnable.EnableMedicine();
        }
    }
    // Update is called once per frame
    public void ablegetantidote()
    {
        CurrentCharacter.SendTrigger("enable", false);
    }
    public void OnGoalComplete(string brainName, string trigger)
    {
        Debug.Log(trigger);
        if (trigger == "able")
        {
            CurrentCharacter.SendTrigger("get", false);
            MedicineEnable.EnableMedicine();
        }
        else if (trigger == "cureinform" && mission == true)
        {
            mission = false;
            missionControl.FinishAskDoctorForCure();
        }
        else if (trigger == "herbinform")
        {
            if (firsec)
            {
                allinform = true;
                CurrentCharacter.SendTrigger("mint0", false);
            }
            firsec = !firsec;
        }
        else if (trigger == "mint0")
        {
            if (firsec)
            {
                CurrentCharacter.SendTrigger("mint1", false);
            }
            firsec = !firsec;
        }
        else if (trigger == "mint1" && allinform == true)
        {
            if (firsec)
            {
                CurrentCharacter.SendTrigger("bloom0", false);
            }
            firsec = !firsec;
        }
        else if (trigger == "bloom0")
        {
            if (firsec)
            {
                CurrentCharacter.SendTrigger("bloom1", false);
            }
            firsec = !firsec;
        }
        else if (trigger == "bloom1" && allinform == true)
        {
            if (firsec)
            {
                CurrentCharacter.SendTrigger("berry0", false);
            }
            firsec = !firsec;
        }
        else if (trigger == "berry0")
        {
            if (firsec)
            {
                CurrentCharacter.SendTrigger("berry1", false);
            }
            firsec = !firsec;
        }
        else if (trigger == "berry1")
        {
            allinform = false;
        }
    }
}
