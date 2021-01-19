using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class CollisionGroundTutorial : MonoBehaviour 
{
    void OnTriggerEnter (Collider col)
    {
        if(col.gameObject.tag == "Boule")
        {
            Destroy(col.gameObject);
        }
    }
}