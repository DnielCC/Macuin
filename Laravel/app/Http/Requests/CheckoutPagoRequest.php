<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CheckoutPagoRequest extends FormRequest
{
    public function authorize(): bool
    {
        return auth()->check();
    }

    public function rules(): array
    {
        return [
            'calle_principal' => ['required', 'string', 'min:3', 'max:150'],
            'num_ext' => ['required', 'string', 'max:10'],
            'num_int' => ['nullable', 'string', 'max:10'],
            'colonia' => ['required', 'string', 'min:2', 'max:100'],
            'municipio' => ['required', 'string', 'min:2', 'max:100'],
            'estado' => ['required', 'string', 'min:2', 'max:100'],
            'cp' => ['required', 'string', 'regex:/^\d{4,5}$/'],
            'referencias' => ['nullable', 'string', 'max:500'],
            'titular_tarjeta' => ['required', 'string', 'min:3', 'max:120'],
            'numero_tarjeta' => ['required', 'string', 'regex:/^\d{16}$/'],
            'expira' => ['nullable', 'string', 'max:7'],
            'cvv' => ['nullable', 'string', 'max:4'],
        ];
    }

    public function messages(): array
    {
        return [
            'cp.regex' => 'El código postal debe tener 4 o 5 dígitos.',
            'calle_principal.required' => 'Indica la calle de envío.',
            'colonia.required' => 'Indica la colonia.',
        ];
    }

    protected function prepareForValidation(): void
    {
        $n = preg_replace('/\D/', '', (string) $this->input('numero_tarjeta', ''));
        $this->merge(['numero_tarjeta' => $n]);
    }
}
