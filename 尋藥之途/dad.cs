using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Inworld;

public class dad : MonoBehaviour
{
    [SerializeField] InworldCharacter CurrentCharacter;
    public GameObject ChangeSceneEffect;
    public string scenename;
    public bool able;
    private bool ending=false;
    public bool mission = true;
    public MissionControl missionControl;
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("start");
        if (able)
        {
            Debug.Log("enable");
            CurrentCharacter.SendTrigger("enable", false);
        }
        else
        {
            Debug.Log("init");
            CurrentCharacter.SendTrigger("init", false);
        }
    }
    private void Update()
    {
        if (Input.GetKey("z"))
        {
            Debug.Log("z");
            ablecure();
        }
    }
    // Update is called once per frame
    public void ablecure()
    {
        CurrentCharacter.SendTrigger("enable", false);
    }
    public void OnGoalComplete(string brainName, string trigger)
    {
        Debug.Log("trigger "+trigger);
        if (trigger == "ask" && mission == true)
        {
            mission = false;
            missionControl.LeaveRoom();
        }
        if (trigger == "able")
        {
            CurrentCharacter.SendTrigger("get", false);
        }
        if (trigger == "get")
        {
            CurrentCharacter.SendTrigger("got", false);
        }
        if (trigger == "got")
        {
            if(ending){
                ChangeSceneEffect.GetComponent<UI>().SceneName = scenename;
                ChangeSceneEffect.GetComponent<Animator>().SetTrigger("ChangeScene");
            }else{
                ending=true;
            }
        }
    }
}
