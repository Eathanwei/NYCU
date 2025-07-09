using GLTFast.Schema;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PCaction : MonoBehaviour
{
    public float moveSpeed = 10f;
    public float rotateSpeed = 100f;
    private Rigidbody rb;
    CharacterController controller;
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        controller = GetComponent<CharacterController>();
    }
    void FixedUpdate()
    {
        HandleMovement();
    }

    void HandleMovement()
    {
        float verticalMove = Input.GetAxis("Vertical") * moveSpeed * Time.deltaTime;
        float horizontalMove = Input.GetAxis("Horizontal") * moveSpeed * Time.deltaTime;

        float rotate = 0f;
        if (Input.GetKey(KeyCode.L)) Application.Quit();
        if (Input.GetKey(KeyCode.Z)) rotate = -1f;
        if (Input.GetKey(KeyCode.C)) rotate = 1f;
        rotate *= rotateSpeed * Time.deltaTime;

        Vector3 movement = transform.forward * verticalMove + transform.right * horizontalMove;
        if (movement.magnitude > 1f)
        {
            movement = movement.normalized;
        }
        controller.Move(movement * moveSpeed * Time.deltaTime);

        transform.Rotate(Vector3.up * rotate);
    }


}
