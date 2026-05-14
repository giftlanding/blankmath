import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useParams } from "@tanstack/react-router";
import { ArrowLeft, FileDown, Layers, ListChecks } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { generateWorksheet } from "../api";
import {
  defaultsForWorksheet,
  schemaForWorksheet,
  WorksheetControl,
  worksheetById,
} from "../worksheetDefinitions";

type FormValues = Record<string, unknown>;

export function WorksheetPage() {
  const { worksheetId } = useParams({ from: "/$worksheetId" });
  const worksheet = worksheetById.get(worksheetId);

  if (!worksheet) {
    return (
      <section className="narrow-page">
        <Link to="/" className="back-link">
          <ArrowLeft size={16} /> Back
        </Link>
        <h1>Worksheet not found</h1>
      </section>
    );
  }

  const form = useForm<FormValues>({
    resolver: zodResolver(schemaForWorksheet(worksheet)),
    defaultValues: defaultsForWorksheet(worksheet),
    mode: "onChange",
  });

  const mutation = useMutation({
    mutationFn: generateWorksheet,
    onSuccess: (result) => {
      if (result.url) {
        window.location.assign(result.url);
      }
    },
  });

  const submit = form.handleSubmit((options) => {
    mutation.mutate({
      worksheetType: worksheet.id,
      options: options as Record<string, string | number | boolean>,
    });
  });

  return (
    <section className="worksheet-page">
      <Link to="/" className="back-link">
        <ArrowLeft size={16} /> Back
      </Link>
      <div className="worksheet-layout">
        <div className="worksheet-summary">
          <span className="category-label">{worksheet.category}</span>
          <h1>{worksheet.title}</h1>
          <p>Printable practice with adjustable format, count, and number settings.</p>
          <div className="worksheet-facts" aria-label="Worksheet configuration facts">
            <span>
              <Layers aria-hidden="true" size={17} />
              {worksheet.examples.length} example{worksheet.examples.length === 1 ? "" : "s"}
            </span>
            <span>
              <ListChecks aria-hidden="true" size={17} />
              {worksheet.controls.length} controls
            </span>
          </div>
          <div className="examples">
            <span className="panel-label">Examples</span>
            {worksheet.examples.map((example) => (
              <code key={example}>{example}</code>
            ))}
          </div>
        </div>

        <form className="worksheet-form" onSubmit={submit}>
          <div className="form-heading">
            <div>
              <span className="section-kicker">Worksheet options</span>
              <h2>Generate a PDF</h2>
            </div>
            <span className="request-badge">{worksheet.id}</span>
          </div>
          <div className="form-grid">
            {worksheet.controls.map((control) => (
              <ControlField key={control.id} control={control} register={form.register} />
            ))}
          </div>

          {form.formState.errors.to && (
            <p className="form-error">{String(form.formState.errors.to.message)}</p>
          )}

          {mutation.isError && <p className="form-error">{mutation.error.message}</p>}

          <button className="generate-button" disabled={!form.formState.isValid || mutation.isPending} type="submit">
            {mutation.isPending ? (
              "Generating..."
            ) : (
              <>
                <FileDown size={18} /> Create PDF
              </>
            )}
          </button>
        </form>
      </div>
    </section>
  );
}

function ControlField({
  control,
  register,
}: {
  control: WorksheetControl;
  register: ReturnType<typeof useForm<FormValues>>["register"];
}) {
  if (control.type === "checkbox") {
    return (
      <label className="checkbox-field">
        <input type="checkbox" {...register(control.id)} />
        <span>{control.label}</span>
      </label>
    );
  }

  if (control.type === "number") {
    return (
      <label className="field">
        <span>{control.label}</span>
        <input type="number" min={control.min} max={control.max} {...register(control.id)} />
      </label>
    );
  }

  return (
    <label className="field">
      <span>{control.label}</span>
      <select {...register(control.id)}>
        {control.options.map((option) => (
          <option value={option} key={option}>
            {control.optionLabels?.[String(option)] ?? option}
          </option>
        ))}
      </select>
    </label>
  );
}
