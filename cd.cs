using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class cd : MonoBehaviour
{
    public float startvalue = 1.0f;
    public AudioSource audioSource;
    public ChangeScene changeScene;
    void Start()
    {
        changeScene = FindObjectOfType<ChangeScene>();
    }
    private void Update()
    {
        transform.Rotate(Vector3.right * 90.0f * Time.deltaTime);
    }
    //private void OnTriggerExit(Collider other)
    //{
    //    changescene();
    //}
    public void changescene()
    {
        PlayerPrefs.SetInt("Level", GameObject.Find("LevelControl").GetComponent<SetLevel>().level);
        StartCoroutine(changeBgm());
        changeScene.StartAnimation("Movie");
        // SceneManager.LoadScene("Movie");
    }
    IEnumerator changeBgm()
    {
        float value = startvalue;
        float diff = startvalue / 10;
        while(value > 0)
        {
            value -= diff;
            audioSource.volume = value;
            yield return new WaitForSeconds(0.1f);
        }
    }
}
