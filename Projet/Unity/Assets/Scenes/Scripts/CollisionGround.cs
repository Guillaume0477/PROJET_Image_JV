using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;
public class CollisionGround : MonoBehaviour 
{
    void OnCollisionEnter (Collision col)
    {
        if(col.gameObject.tag == "Boule"){
            Destroy(col.gameObject);
        }
    }

    void Update ()
	{
        
	}
}