using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

public class deco : MonoBehaviour
{
    public Vector3[] move;
    public GameObject ontree;
    private gifts giftplace;
    private void Start()
    {
        giftplace = GameObject.Find("aroundtree").GetComponent<gifts>();
    }
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.name == "place1")
        {
            other.gameObject.SetActive(false);
            ontree.transform.position = move[0];
            ontree.SetActive(true);
            gameObject.SetActive(false);
            giftplace.decos();
        }
        else if (other.gameObject.name == "place2")
        {
            other.gameObject.SetActive(false);
            ontree.transform.position = move[1];
            ontree.SetActive(true);
            gameObject.SetActive(false);
            giftplace.decos();
        }
        else if (other.gameObject.name == "place3")
        {
            other.gameObject.SetActive(false);
            ontree.transform.position = move[2];
            ontree.SetActive(true);
            gameObject.SetActive(false);
            giftplace.decos();
        }
        else if (other.gameObject.name == "place4")
        {
            other.gameObject.SetActive(false);
            ontree.transform.position = move[3];
            ontree.SetActive(true);
            gameObject.SetActive(false);
            giftplace.decos();
        }
        else if (other.gameObject.name == "place5")
        {
            other.gameObject.SetActive(false);
            ontree.transform.position = move[4];
            ontree.SetActive(true);
            gameObject.SetActive(false);
            giftplace.decos();
        }
        else if (other.gameObject.name == "place6")
        {
            other.gameObject.SetActive(false);
            ontree.transform.position = move[5];
            ontree.SetActive(true);
            gameObject.SetActive(false);
            giftplace.decos();
        }
    }
}
