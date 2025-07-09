using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Inworld;

public class merchant : MonoBehaviour
{
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
        if (Input.GetKey("x"))
        {
            Debug.Log("x");
            ablebuyberry();
        }
        if (Input.GetKey("e"))
        {
            Shop.EnableShopHerb();
        }
    }
    // Update is called once per frame
    public void ablebuyberry()
    {
        CurrentCharacter.SendTrigger("enable", false);
    }
    public void OnGoalComplete(string brainName, string trigger)
    {
        Debug.Log(trigger);
        if (trigger == "able")
        {
            CurrentCharacter.SendTrigger("get", false);
            Shop.EnableShopHerb();
        }
        else if(trigger == "unable" && mission == true)
        {
            mission = false;
            missionControl.FinishAskMerchantForBerry();
        }
    }
}
