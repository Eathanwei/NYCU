using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class weight : MonoBehaviour
{
    public BalanceController balance;
    public int objectweight;
    public int category;
    // Start is called before the first frame update
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.name == "Left")
        {
            balance.leftweight += objectweight;
        }
        else if (other.gameObject.name == "Right")
        {
            balance.rightweight += objectweight;
        }
        else if (other.gameObject.name == "Plate")
        {
            balance.onplates(category,1);
        }
    }
    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.name == "Left")
        {
            balance.leftweight -= objectweight;
        }
        else if (other.gameObject.name == "Right")
        {
            balance.rightweight -= objectweight;
        }
        else if (other.gameObject.name == "Plate")
        {
            balance.onplates(category,-1);
        }
    }
}
