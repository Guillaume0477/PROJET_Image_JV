using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyStats : MonoBehaviour 
{
    public int ennemyHealth = 100;


	void OnCollisionEnter (Collision col)
	{
        if(col.gameObject.tag == "Boule"){
            ennemyHealth -= 50;
        }
    }

	void Update ()
	{
        if(ennemyHealth <= 0){
			Dead();
		}
	}

	void Dead(){
		Destroy (gameObject, 0.001f);
	}

	public int getHealth ()
	{
		return(ennemyHealth);
    }
}