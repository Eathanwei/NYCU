using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class CameraVerticalRotate : MonoBehaviour
{
    private float rotateSpeed = 45f;
    private float verticalAngle = 0f;
    public GameObject heldObject;
    public Camera mainCamera;
    private float followSpeed = 10f;
    public float fixedDistance = 1f;
    private Ray ray;
    public cd cdObject;
    private Rigidbody heldObjectRigidbody;
    private Vector3 targetPos;
    private Vector3 heldObjectPosition;
    private float input = 0f;
    private void Start()
    {
        if (PlayerPrefs.GetInt("Level", 0) == 6)
        {
            Debug.Log("666");
            verticalAngle = Mathf.Clamp(30, -75f, 75f);
            Vector3 currentRotation = transform.eulerAngles;
            currentRotation.x = verticalAngle;
            transform.eulerAngles = currentRotation;
        }
    }
    void Update()
    {
        input = 0f;
        if (Input.GetKey(KeyCode.E))
            input = 1f;
        else if (Input.GetKey(KeyCode.Q))
            input = -1f;
        verticalAngle += input * rotateSpeed * Time.deltaTime;
        verticalAngle = Mathf.Clamp(verticalAngle, -75f, 75f);
        Vector3 currentRotation = transform.eulerAngles;
        currentRotation.x = verticalAngle;
        transform.eulerAngles = currentRotation;

        ray = mainCamera.ScreenPointToRay(Input.mousePosition);
        if (Input.GetMouseButtonDown(0))
        {
            Debug.DrawRay(ray.origin, ray.direction * 100f, Color.red, 2f);
            if (heldObject == null)
            {
                LayerMask paintLayerMask = 1 << LayerMask.NameToLayer("paint");
                if (Physics.Raycast(ray, out RaycastHit hit, 100f, paintLayerMask))
                {
                    if (hit.collider.CompareTag("Pickup"))
                    {
                        heldObject = hit.collider.gameObject;
                        heldObject.transform.rotation = Quaternion.identity;
                        heldObjectRigidbody = heldObject.GetComponent<Rigidbody>();
                        heldObjectRigidbody.useGravity = false;
                        heldObjectRigidbody.freezeRotation = true;
                        heldObjectRigidbody.collisionDetectionMode = CollisionDetectionMode.ContinuousSpeculative;
                        //heldObjectRigidbody.isKinematic = true;
                    }
                    else if (hit.collider.CompareTag("pianokey"))
                    {
                        hit.collider.gameObject.GetComponent<PianoKeyBoard>().mouseClickPianoKey();
                    }
                    else if (hit.collider.CompareTag("baby"))
                    {
                        hit.collider.gameObject.GetComponent<baby>().changescene.StartAnimation("Menu");
                    }
                }
                else if (Physics.Raycast(ray, out RaycastHit hit2))
                {
                    if (hit2.collider.CompareTag("Pickup"))
                    {
                        heldObject = hit2.collider.gameObject;
                        heldObject.transform.rotation = Quaternion.identity;
                        heldObjectRigidbody = heldObject.GetComponent<Rigidbody>();
                        heldObjectRigidbody.useGravity = false;
                        heldObjectRigidbody.freezeRotation = true;
                        heldObjectRigidbody.collisionDetectionMode = CollisionDetectionMode.ContinuousSpeculative;
                        //heldObjectRigidbody.isKinematic = true;
                    }
                    else if (hit2.collider.CompareTag("cd"))
                    {
                        cdObject.changescene();
                    }
                    else if (hit2.collider.CompareTag("doorKnob"))
                    {
                        if (PlayerPrefs.GetInt("Level", 0) == hit2.collider.gameObject.GetComponent<doorValue>().level)
                        {
                            Transform door = hit2.collider.transform.parent;
                            StartCoroutine(OpenDoorSmoothly(door, true));
                        }
                    }
                    else if (hit2.collider.CompareTag("doorKnob2"))
                    {
                        if (PlayerPrefs.GetInt("Level", 0) == hit2.collider.gameObject.GetComponent<doorValue>().level)
                        {
                            Transform door = hit2.collider.transform.parent;
                            StartCoroutine(OpenDoorSmoothly(door, false));
                        }
                    }
                }
            }
            else
            {
                //heldObjectRigidbody.isKinematic = false;
                heldObjectRigidbody.useGravity = true;
                heldObjectRigidbody.freezeRotation = false;
                heldObjectRigidbody.collisionDetectionMode = CollisionDetectionMode.Discrete;
                heldObject = null;
            }
        }
    }
    void FixedUpdate()
    {
        if (heldObject != null)
        {
            targetPos = ray.origin + ray.direction.normalized * fixedDistance;
            //heldObject.transform.position = Vector3.Lerp(heldObject.transform.position, targetPos, Time.deltaTime * followSpeed);
            heldObjectPosition = Vector3.Lerp(heldObjectRigidbody.position, targetPos, Time.deltaTime * followSpeed);
            heldObjectRigidbody.MovePosition(heldObjectPosition);
        }
    }
    IEnumerator OpenDoorSmoothly(Transform door, bool direction)
    {
        HingeJoint hinge = door.GetComponent<HingeJoint>();
        hinge.useMotor = true;
        JointMotor motor = hinge.motor;
        motor.force = 100f;
        if(direction)
        {
            motor.targetVelocity = -90f;
        }
        else
        {
            motor.targetVelocity = 90f;
        }
        motor.freeSpin = false;

        hinge.motor = motor;

        yield return new WaitForSeconds(1f);

        motor.targetVelocity = 0f;
        hinge.motor = motor;
        hinge.useMotor = false;
    }
}
