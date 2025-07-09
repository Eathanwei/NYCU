using SojaExiles;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class frame : MonoBehaviour
{
    public int is_paint = 0;
    public int is_draw = 0;
    public Vector3 move;
    public Vector3 rotate;
    public Vector3 movecd;
    public frame otherframe;
    public GameObject cd;
    private GameObject newpaint;
    private void OnTriggerEnter(Collider other)
    {
        Debug.Log(other.name + " Enter");
        if (other.gameObject.name == "Paint 1" && is_draw==0)
        {
            is_paint = 1;
            is_draw=1;
            enterframe(other);
        }
        else if (other.gameObject.name == "Paint 2" && is_draw==0)
        {
            is_paint = 2;
            is_draw=2;
            enterframe(other);
        }
        else if (other.gameObject.name == "Paint 3" && is_draw==0)
        {
            is_draw=3;
            enterframe(other);
        }
        else if (other.gameObject.name == "Paint 4" && is_draw==0)
        {
            is_draw=4;
            enterframe(other);
        }
        else if (other.gameObject.name == "Paint 5" && is_draw==0)
        {
            is_draw=5;
            enterframe(other);
        }
        check();
    }
    private void OnTriggerExit(Collider other)
    {
        Debug.Log(other.name + " Exit");
        if (other.gameObject.name == "Paint 1")
        {
            if (is_paint == 1)
            {
                is_paint = 0;
            }
            if(is_draw==1){
                is_draw=0;
            }
            //other.attachedRigidbody.useGravity = true;
        }
        else if (other.gameObject.name == "Paint 2")
        {
            if (is_paint == 2)
            {
                is_paint = 0;
            }
            if(is_draw==2){
                is_draw=0;
            }
            //other.attachedRigidbody.useGravity = true;
        }
        else if (other.gameObject.name == "Paint 3")
        {
            if(is_draw==3){
                is_draw=0;
            }
            //other.attachedRigidbody.useGravity = true;
        }
        else if (other.gameObject.name == "Paint 4")
        {
            if(is_draw==4){
                is_draw=0;
            }
            //other.attachedRigidbody.useGravity = true;
        }
        else if (other.gameObject.name == "Paint 5")
        {
            if(is_draw==5){
                is_draw=0;
            }
            //other.attachedRigidbody.useGravity = true;
        }
    }
    private void enterframe(Collider other)
    {
        
        newpaint = Instantiate(other.gameObject);
        newpaint.name = other.gameObject.name;
        Destroy(other.gameObject);
        newpaint.GetComponent<Rigidbody>().useGravity = false;
        newpaint.transform.position = move;
        newpaint.transform.localEulerAngles = rotate;
    }
    public void check()
    {
        if (is_paint != 0 && otherframe.is_paint != 0)
        {
            Debug.Log("completed!");
            cd.SetActive(true);
            cd.transform.position = movecd;
        }
    }
}
