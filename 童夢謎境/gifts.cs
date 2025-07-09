using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class gifts : MonoBehaviour
{
    public int gift_num = 0;
    public int deco_num = 0;
    public GameObject cd;
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.name == "present_01")
        {
            gift_num++;
        }
        else if (other.gameObject.name == "present_06")
        {
            gift_num++;
        }
        else if (other.gameObject.name == "GiftBox")
        {
            gift_num++;
        }
        check();
    }
    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.name == "present_01")
        {
            gift_num--;
        }
        else if (other.gameObject.name == "present_06")
        {
            gift_num--;
        }
        else if (other.gameObject.name == "GiftBox")
        {
            gift_num--;
        }
    }
    public void decos()
    {
        deco_num++;
        check();
    }
    public void check()
    {
        if (gift_num == 3 && deco_num == 3)
        {
            Debug.Log("completed!");
            cd.SetActive(true);
        }
    }
}
