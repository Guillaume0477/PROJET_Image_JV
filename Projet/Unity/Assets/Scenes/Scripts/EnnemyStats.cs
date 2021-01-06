using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyStats : MonoBehaviour {

	private PlayerController player;
	// Create public variables for player speed, and for the Text UI game objects
    public int ennemyHealth = 100;

	// At the start of the game..
	void OnCollisionEnter (Collision col)
	{
        if(col.gameObject.tag == "Boule"){
            ennemyHealth -= 50;
        }
    }

	// Each physics step..
	void Update ()
	{
        if(ennemyHealth <= 0){
			Dead();
		}
	}

	void Dead(){
		Destroy (gameObject, 0.001f);
	}
}