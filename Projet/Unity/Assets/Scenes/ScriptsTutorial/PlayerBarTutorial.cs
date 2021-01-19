using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerBarTutorial : MonoBehaviour 
{
    public Slider slider;

    public void SetMaxValue(float maxValue)
    {
        slider.maxValue = maxValue;
        slider.value = maxValue;
    }

    public void SetValue(float value)
    {
        slider.value = value;
    }
}