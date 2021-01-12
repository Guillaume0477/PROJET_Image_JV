using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerStats : MonoBehaviour {
	
	// Create public variables for player speed, and for the Text UI game objects
    private float health = 100;
	private float mana = 100;
	private float healthMax = 100;
	private float manaMax = 100;

	public void ApplyDammage (float TheDammage)
	{
        health -= TheDammage;

        if(health <= 0)
		{
			health = 0;
        }
    }

	public void ApplyMana (float Mana)
	{
        mana -= Mana;
        
        if(mana <= 0)
		{
			mana = 0;
        }
    }

	public void RegenerateMana (float Mana)
	{
        mana += Mana;
        
        if(mana >= 100)
		{
			mana = 100;
        }
    }

	public float getHealth ()
	{
		return(health);
    }

	public float getMana ()
	{
		return(mana);
    }

	public float getHealthMax ()
	{
		return(healthMax);
    }

	public float getManaMax ()
	{
		return(manaMax);
    }
}