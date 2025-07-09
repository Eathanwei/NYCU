using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class baby : MonoBehaviour
{
    // public AudioSource audioSource;
    public ChangeScene changescene;
    private void OnTriggerEnter(Collider other)
    {
        Debug.Log("completed");
        // StartCoroutine(changeBgm());
        changescene.StartAnimation("Menu");
    }
    // IEnumerator changeBgm()
    // {
    //     float value = 1.0f;
    //     while(value > 0)
    //     {
    //         value -= 0.1f;
    //         audioSource.volume = value;
    //         yield return new WaitForSeconds(0.1f);
    //     }
        
    // }
}
